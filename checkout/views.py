from django.shortcuts import render, redirect, reverse, \
                             get_object_or_404, HttpResponse
from django.views import View
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib import messages

from .models import Order, OrderLineItem
from .forms import ContactDetailsForm, BillingDetailsForm
from .order import create_order
from core.contexts import get_base_context, get_product_by_name, \
                          handle_server_errors
from core.shortcuts import price_as_float, is_tomorrows_date
from cart.cartfunctions import has_reached_cutoff_time
from profiles.models import UserProfile
from contact.models import NewsletterEmails, DiscountCode
from contact.views import NewsletterSignup

import stripe
import json
from datetime import datetime


class Checkout(View):
    template = 'checkout/checkout.html'

    @handle_server_errors
    def get(self, request):
        cart = None
        if 'cart' in request.session:
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

        contact_details = {}
        billing_details = {}
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(
                    user=request.user
                )
                contact_details = {
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'email': request.user.email,
                    'phone': profile.saved_phone_number
                }
                billing_details = {
                    'street_address1': profile.saved_street_address1,
                    'street_address2': profile.saved_street_address2,
                    'town_or_city': profile.saved_town_or_city,
                    'county': profile.saved_county,
                    'postcode': profile.saved_postcode
                }
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=request.user)
                messages.warning(
                    request,
                    """Your profile information was missing.
                    Any data previously saved has been cleared."""
                )
        contact_form = ContactDetailsForm(initial=contact_details)
        billing_form = BillingDetailsForm(initial=billing_details)

        context = get_base_context(request)
        context['contact_form'] = contact_form
        context['billing_form'] = billing_form
        context['stripe_public_key'] = stripe_public_key
        context['client_secret'] = intent.client_secret
        context['grand_total'] = price_as_float(grand_total)

        # Adding a checkbox to subscribe to the newsletter
        try:
            newsletter_email = NewsletterEmails.objects.get(
                email=request.user.email
            )
            if not newsletter_email.is_active:
                raise Exception
        except Exception:
            context['newsletter_checkbox'] = True

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

    @handle_server_errors
    def post(self, request):
        """
        Submits an order on payment
        """
        cart = request.session['cart']
        order_context = request.session.get('order_context', {})

        bake_date = order_context['bake_date']
        customer_note = order_context.get('customer_note', '')
        is_delivery = 'delivery' in request.POST

        checkout_data = request.POST.copy()
        checkout_data['full_name'] = (
            f"""{checkout_data['first_name']} {checkout_data['last_name']}""")

        checkout_data.update({
            'bake_date': bake_date,
            'customer_note': customer_note
        })

        pid = request.POST.get('client_secret').split('_secret')[0]
        checkout_data['stripe_pid'] = pid
        checkout_data['discount'] = request.session.pop('discount', 0)

        # Overriding any unwanted inputs
        if is_delivery and 'delivery_other_address' not in request.POST:
            checkout_data.update({
                'delivery_line1': None,
                'delivery_city': None,
                'delivery_county': None,
                'delivery_postcode': None
            })

        # Updating the user profile if save info is checked
        user = None
        if request.user.is_authenticated:
            user = request.user
        save_info = 'save_info' in request.POST and user

        order = create_order(checkout_data, cart, save_info, user)

        request.session['cart'].clear()
        request.session['cart_total'] = 0

        # Confirmation toasts
        messages.success(request, f"""Your payment was successful! A
            confirmation email has been sent to {order.email}.""")
        if save_info:
            messages.success(request, """Your billing information has
                been saved!""")

        # Signing up for the newsletter
        if 'newsletter_subscribe' in request.POST:
            response = NewsletterSignup.subscribe_email(
                request.POST['email'])

            if response == 'Email already active':
                messages.info(request, """Your email is already
                    subscribed to the newsletter.""")
            elif response == 'New subscription':
                messages.success(request,
                                 'You have signed up for our newsletter!')
            elif response == 'Subscription reactivated':
                messages.success(request, """
                    'Your newsletter subscription has been
                    reactivated!""")
            else:
                messages.error(request, f"""Failed to sign up
                    with newsletter. {response}""")

        return redirect(reverse('checkout_success',
                                args=[order.order_number]))


class CheckoutSuccess(View):
    template = 'checkout/checkout_success.html'

    @handle_server_errors
    def get(self, request, order_no):
        context = get_base_context(request)
        order = get_object_or_404(Order, order_number=order_no)
        context['order'] = order
        save_info = request.session.get('save_info')

        return render(request, self.template, context)


@require_POST
def cache_checkout_data(request):
    # Validate the form before processing the payment
    contact_form = ContactDetailsForm(request.POST)
    billing_form = BillingDetailsForm(request.POST)

    if not contact_form.is_valid() or not billing_form.is_valid():
        messages.error(request, "Your form is invalid. \
            Please double check your details")
        return HttpResponse(status=400)

    bake_date = ''
    customer_note = ''
    if 'order_context' in request.session:
        order_context = request.session['order_context']
        bake_date = order_context['bake_date']
        customer_note = order_context.get('customer_note', '')

        # The final check to ensure the next day bake date is valid
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

        # Updating the payment amount to include the delivery
        cart_total = request.session['cart_total']
        discount = 0
        if 'code_name' in request.POST:
            try:
                newsletter = NewsletterEmails.objects.get(
                    email=request.POST['email']
                )
                discount_code = newsletter.received_codes.get(
                    code_name=request.POST['code_name']
                )
                discount = discount_code.get_discount(cart_total)
                newsletter.received_codes.remove(discount_code)
                newsletter.save()
                request.session['discount'] = discount
            except Exception:
                # Because we already validated the discount code, this
                # can only happen if the user uses the code in another
                # tab
                messages.error(
                    request,
                    "Your discount code is no longer available"
                )
                return HttpResponse(content='Invalid code', status=400)

        delivery = 'delivery' in request.POST
        delivery_other_address = 'delivery_other_address' in request.POST
        delivery_cost = 0
        if delivery:
            delivery_county = request.POST['delivery_county'] \
                if delivery_other_address \
                else request.POST['county']
            delivery_cost = settings.COUNTY_DELIVERY_COSTS[
                delivery_county
            ]
        grand_total = cart_total - discount + delivery_cost

        metadata = {
            'user': request.user.id,
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'bake_date': bake_date,
            'customer_note': customer_note,
            'save_info': request.POST.get('save_info'),
            'discount': discount,
            'delivery': delivery,
            'delivery_other_address': delivery_other_address
        }
        # Saving the original billing postcode as it is overwritten by Stripe
        if delivery_other_address:
            metadata['billing_postcode'] = request.POST['postcode']
        if 'newsletter_subscribe' in request.POST:
            metadata['newsletter_subscribe'] = 'true'

        # Adding each item as its own key to avoid the 500 character limit
        cart = request.session.get('cart', {})
        for count, item in enumerate(cart):
            # Removing the unnecessary information in the product dict
            item_data = {**item}
            item_data['prop_list'] = {
                prop['name']: prop['answer'] for prop in item['prop_list']
            }
            metadata[f'product_{count}'] = json.dumps(item_data)

        stripe.PaymentIntent.modify(
            pid,
            metadata=metadata,
            amount=grand_total
        )

        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f"""
            Sorry, but your payment cannot be processed.
            Please try again. {e}
            """)
        return HttpResponse(content=e, status=400)


@require_POST
def get_discount_code(request):
    """
    Gets the discount code entered by the user at checkout
    """
    try:
        newsletter_email = NewsletterEmails.objects.get(
            email=request.POST['email']
        )
        discount_code = newsletter_email.received_codes.get(
            code_name=request.POST['code_name']
        )
        # Calculating the discount
        cart_total = request.session['cart_total']
        discount = None

        if discount_code.min_spending > cart_total:
            return HttpResponse(
                content=f"""Your cart needs to be at least
                    €{discount_code.min_spending} for this
                    code to be applied""",
                status=400
            )
        discount = discount_code.get_discount(cart_total)

        response_data = json.dumps({
            'discount': price_as_float(discount),
            'new_total': price_as_float(cart_total - discount)
        })
        return HttpResponse(
            content=response_data,
            status=200
        )

    except NewsletterEmails.DoesNotExist:
        return HttpResponse(
            content='Your email has no discount codes available',
            status=400)
    except DiscountCode.DoesNotExist:
        return HttpResponse(
            content='You do not have that discount code',
            status=400)
    except Exception as e:
        return HttpResponse(content=e, status=400)
