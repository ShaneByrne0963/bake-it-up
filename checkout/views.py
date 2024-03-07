from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from django.contrib import messages

from .forms import CheckoutForm
from core.contexts import get_base_context
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
        print(intent)

        context = get_base_context(request)
        context['form'] = CheckoutForm()
        context['stripe_public_key'] = stripe_public_key
        context['client_secret'] = intent.client_secret
        context['grand_total'] = price_as_float(grand_total)

        return render(request, self.template, context)
    
    def post(self, request):
        return redirect('checkout_success')


class CheckoutSuccess(View):
    template = 'checkout/checkout_success.html'

    def get(self, request):
        context = get_base_context(request)

        return render(request, self.template, context)
