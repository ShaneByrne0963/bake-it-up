from django.shortcuts import render
from django.views import View
from django.conf import settings

from .forms import CheckoutForm
from core.contexts import get_base_context


class Checkout(View):
    template = 'checkout/checkout.html'

    def get(self, request):
        context = get_base_context(request)
        context['form'] = CheckoutForm()
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        context['client_secret'] = '12_secret_891237564r875jduihfu'

        return render(request, self.template, context)
