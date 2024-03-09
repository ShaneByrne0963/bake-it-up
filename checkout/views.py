from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.conf import settings
from django.contrib import messages

from .models import Order, OrderLineItem
from .forms import CheckoutForm
from core.contexts import get_base_context, get_product_by_name
from core.shortcuts import price_as_float

import stripe


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
        context['form'] = CheckoutForm()
        context['stripe_public_key'] = stripe_public_key
        context['client_secret'] = intent.client_secret
        context['grand_total'] = price_as_float(grand_total)

        return render(request, self.template, context)
    
    def post(self, request):
        """
        Submits an order on payment
        """
        cart = request.session.get('cart', [])

        checkout_data = {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'phone': request.POST['phone'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'postcode': request.POST['postcode'],
        }
        checkout_form = CheckoutForm(checkout_data)
        if checkout_form.is_valid():
            order = Order(
                full_name=checkout_data['name'],
                email=checkout_data['email'],
                phone_number=checkout_data['phone'],
                street_address1=checkout_data['street_address1'],
                street_address2=checkout_data['street_address2'],
                town_or_city=checkout_data['town_or_city'],
                county=checkout_data['county'],
                postcode=checkout_data['postcode']
            )
            order.save()

            for item in cart:
                # Getting custom properties, with None as a default
                properties = {
                    'shape': None,
                    'size': None,
                    'contents': None,
                    'type': None,
                    'color': None,
                    'icing': None,
                    'decoration': None,
                    'text': None
                }
                for prop in item['prop_list']:
                    properties[prop['name']] = prop['answer']

                line_item = OrderLineItem(
                    order=order,
                    product_name=item['name'],
                    quantity=item['quantity'],
                    prop_shape=properties['shape'],
                    prop_size=properties['size'],
                    prop_contents=properties['contents'],
                    prop_type=properties['type'],
                    prop_color=properties['color'],
                    prop_icing=properties['icing'],
                    prop_decoration=properties['decoration'],
                    prop_text=properties['text'],
                )
                line_item.save()
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
