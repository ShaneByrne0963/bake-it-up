from django.http import HttpResponse
from django.contrib.auth.models import User

from .order import create_order
from .models import Order

from contact.views import NewsletterSignup

import stripe
import time
import json


class StripeWH_Handler():
    """
    Handles Stripe webhooks
    """

    def __init__(self, request):
        self.request = request
    
    def handle_payment_intent_succeeded(self, event):
        """
        Handles the payment_intent.succeeded webhook
        """
        intent = event.data.object
        pid = intent.id
        
        attempt = 1
        while attempt < 5:
            try:
                order = Order.objects.get(stripe_pid=pid)
            
                return HttpResponse(
                    content=f"""Webhook received: {event['type']}.
                    Order already exists in database""",
                    status=200
                )
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        
        # Extracting the metadata from the payment intent
        save_info = (intent.metadata.save_info == 'on')
        bake_date = intent.metadata.bake_date
        discount = int(intent.metadata.discount)
        delivery = (intent.metadata.delivery == 'True')
        delivery_other_address = (
            intent.metadata.delivery_other_address == 'True')
        customer_note = getattr(intent.metadata, 'customer_note',
                                '')

        # Getting the user to save their profile information
        user = None
        try:
            user_id = int(intent.metadata.user)
            user = User.objects.get(pk=user_id)
        except:
            save_info = False

        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )
        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = stripe_charge.amount

        # Subscribe to the newsletter
        if hasattr(intent.metadata, 'newsletter_subscribe'):
            NewsletterSignup.subscribe_email(billing_details.email)

        # Replacing empty strings with None
        for key, value in shipping_details.address.items():
            if value == '':
                shipping_details.address[key] = None

        order = None
        try:
            # Extracting the cart from the payment intent metadata
            cart = []
            unordered_cart = {}
            number_of_products = 0
            for key, value in intent.metadata.items():
                if not 'product_' in key:
                    continue
                number_of_products += 1
                product_number = key.replace('product_', '')
                item_data = json.loads(value)

                # Formatting the data from the payment intent
                old_properties = {**item_data['prop_list']}
                item_data['prop_list'] = []

                for key, value in old_properties.items():
                    item_data['prop_list'].append({
                        'name': key,
                        'answer': value
                    })
                unordered_cart[product_number] = item_data

            # Ordering the products the way they are in the user cart
            for i in range(number_of_products):
                cart.append(unordered_cart[str(i)])

            # Getting the checkout shipping details to fill into the new order
            checkout_data = {
                'bake_date': bake_date,
                'customer_note': customer_note,
                'discount': discount,
                'delivery': delivery,
                'name': billing_details.name,
                'email': billing_details.email,
                'phone': billing_details.phone,
                'street_address1': billing_details.address.line1,
                'street_address2': billing_details.address.line2,
                'town_or_city': billing_details.address.city,
                'county': billing_details.address.state,
                'postcode': shipping_details.address.postal_code,
                'pid': pid,
                'delivery_line1': None,
                'delivery_line2': None,
                'delivery_city': None,
                'delivery_county': None,
                'delivery_postcode': None
            }
            if delivery_other_address:
                checkout_data.update({
                    'postcode': intent.metadata.billing_postcode,
                    'delivery_line1': shipping_details.address.line1,
                    'delivery_line2': shipping_details.address.line2,
                    'delivery_city': shipping_details.address.city,
                    'delivery_county': shipping_details.address.state,
                    'delivery_postcode': shipping_details.address.postal_code
                })
            order = create_order(checkout_data, cart, save_info, user)

            return HttpResponse(
                content=f"""Webhook received: {event['type']}.
                Order created in webhook""",
                status=200
            )
        except Exception as e:
            if order:
                order.delete()

            return HttpResponse(
                content=f"""Webhook received: {event['type']}.
                | ERROR: {e}""",
                status=500
            )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handles the payment_intent.payment_failed webhook
        """
        return HttpResponse(
            content=f"Failed webhook received: {event['type']}",
            status=200
        )

    def handle_event(self, event):
        """
        Handles a Stripe webhook event
        """
        return HttpResponse(
            content=f"Unhandled webhook received: {event['type']}",
            status=200
        )