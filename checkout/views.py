from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views import View
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib import messages

from .models import Order, OrderLineItem
from .forms import ContactDetailsForm, BillingDetailsForm
from .order import create_order
from core.contexts import get_base_context, get_product_by_name
from core.shortcuts import price_as_float, is_tomorrows_date
from cart.cartfunctions import has_reached_cutoff_time

import stripe
import json
from datetime import datetime


class Checkout(View):
    template = 'checkout/checkout.html'

    def get(self, request):
        cart = request.session['cart']
        if not cart:
            messages.add_message(request,
                                 messages.ERROR,
                                 'Your cart is empty')
            return redirect('home')

        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY

        if not stripe_public_key:
            messages.warning(request, """Stripe public key is missing.
                Please check your environment variables""")

        grand_total = request.session['cart_total']
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=grand_total,
            currency=settings.CURRENCY
        )

        context = get_base_context(request)
        context['contact_form'] = ContactDetailsForm()
        context['billing_form'] = BillingDetailsForm()
        context['stripe_public_key'] = stripe_public_key
        context['client_secret'] = intent.client_secret
        context['grand_total'] = price_as_float(grand_total)

        # Get the context to create the select form
        county_options = []
        for county, cost in settings.COUNTY_DELIVERY_COSTS.items():
            parsed_cost = cost
            if cost is not None:
                parsed_cost = price_as_float(cost)

            county_data = {
                'name': county,
                'cost': parsed_cost
            }
            county_options.append(county_data)
        context['county_options'] = county_options

        return render(request, self.template, context)
    
    def post(self, request):
        """
        Submits an order on payment
        """
        cart = request.session['cart']
        order_context = request.session.get('order_context', {})

        bake_date = order_context['bake_date']
        customer_note = order_context.get('customer_note', '')

        checkout_data = {
            'bake_date': bake_date,
            'customer_note': customer_note,
            'name': request.POST['name'],
            'email': request.POST['email'],
            'phone': request.POST['phone'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'postcode': request.POST['postcode'],
        }
        contact_form = ContactDetailsForm(checkout_data)
        billing_form = BillingDetailsForm(checkout_data)

        if contact_form.is_valid() and billing_form.is_valid():
            pid = request.POST.get('client_secret').split('_secret')[0]
            checkout_data['pid'] = pid

            # Adding delivery details, if delivery is selected
            delivery_details = {
                'delivery_line1': None,
                'delivery_line2': None,
                'delivery_city': None,
                'delivery_county': None,
                'delivery_postcode': None
            }
            is_delivery = 'delivery' in request.POST
            checkout_data['delivery'] = is_delivery
            if is_delivery and 'delivery_other_address' in request.POST:
                delivery_details.update({
                    'delivery_line1': request.POST['delivery_line1'],
                    'delivery_city': request.POST['delivery_city'],
                    'delivery_county': request.POST['delivery_county'],
                    'delivery_postcode': request.POST['delivery_postcode']
                })
                if 'delivery_line2' in request.POST:
                    delivery_details['delivery_line2'] = request.POST['delivery_line2']
            checkout_data.update(delivery_details)

            order = create_order(checkout_data, cart)

            save_info = 'save_info' in request.POST
            request.session['save_info'] = save_info
            request.session['cart'].clear()
            request.session['cart_total'] = 0

            messages.success(request, f'Your payment was successful! A \
            confirmation email has been sent to {order.email}.')
            if save_info:
                messages.success(request, 'Your billing information has \
                    been saved!')

            return redirect(reverse('checkout_success', args=[order.order_number]))

        messages.error(request, 'Your information was invalid. Please try again')
        return redirect('checkout')


class CheckoutSuccess(View):
    template = 'checkout/checkout_success.html'

    def get(self, request, order_no):
        context = get_base_context(request)
        order = get_object_or_404(Order, order_number=order_no)
        context['order'] = order
        save_info = request.session.get('save_info')

        return render(request, self.template, context)


@require_POST
def cache_checkout_data(request):
    # The final check to ensure the next day bake date is valid
    bake_date = ''
    customer_note = ''
    if 'order_context' in request.session:
        order_context = request.session['order_context']
        bake_date = order_context['bake_date']
        customer_note = order_context.get('customer_note', '')

        if is_tomorrows_date(bake_date) \
                and has_reached_cutoff_time():
            request.session['global_context'] = {
                'val_note': customer_note,
                'cutoff_reached': True
            }
            messages.error(request, "Sorry, but you have \
                passed the time for next day baking!")
            return HttpResponse(status=403)
    else:
        messages.error(request, 'Your cart details are missing. \
            Please fill them out again')
        return HttpResponse(status=403)

    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY

        metadata = {
            'user': request.user,
            'bake_date': bake_date,
            'customer_note': customer_note,
            'save_info': request.POST.get('save_info')
        }

        # Adding each item as its own key to avoid the 500 character limit
        cart = request.session.get('cart', {})
        for count, item in enumerate(cart):
            metadata[f'product_{count}'] = json.dumps(item)
        stripe.PaymentIntent.modify(pid, metadata=metadata)

        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f"""
        Sorry, but your payment cannot be processed.
        Please try again. {e}
        """)
        return HttpResponse(content=e, status=400)
