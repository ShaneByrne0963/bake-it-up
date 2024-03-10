from django.http import HttpResponse

from .order import create_order
from .models import Order

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

        save_info = intent.metadata.save_info
        bake_date = intent.metadata.bake_date
        customer_note = getattr(
            intent.metadata,
            'customer_note',
            ''
        )

        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )
        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        grand_total = stripe_charge.amount

        for key, value in shipping_details.address.items():
            if value == '':
                shipping_details.address[key] = None
        
        attempt = 1
        while attempt < 5:
            try:
                order = Order.objects.get(stripe_pid=pid)
            
                return HttpResponse(
                    content=f'Webhook received: {event['type']}. \
                    Order already exists in database',
                    status=200
                )
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
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
                unordered_cart[product_number] = json.loads(value)

            # Ordering the products the way they are in the user cart
            for i in range(number_of_products):
                cart.append(unordered_cart[f'{i}'])

            # Getting the checkout shipping details to fill into the new order
            checkout_data = {
                'bake_date': bake_date,
                'customer_note': customer_note,
                'name': shipping_details.name,
                'email': billing_details.email,
                'phone': shipping_details.phone,
                'street_address1': shipping_details.address.line1,
                'street_address2': shipping_details.address.line2,
                'town_or_city': shipping_details.address.city,
                'county': shipping_details.address.state,
                'postcode': shipping_details.address.postal_code,
                'pid': pid
            }
            order = create_order(checkout_data, cart)

            return HttpResponse(
                content=f'Webhook received: {event['type']}. \
                Order created in webhook',
                status=200
            )
        except Exception as e:
            print(e)
            if order:
                order.delete()

            return HttpResponse(
                content=f'Webhook received: {event['type']}. \
                | ERROR: {e}',
                status=500
            )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handles the payment_intent.payment_failed webhook
        """
        return HttpResponse(
            content=f'Failed webhook received: {event['type']}',
            status=200
        )

    def handle_event(self, event):
        """
        Handles a Stripe webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event['type']}',
            status=200
        )