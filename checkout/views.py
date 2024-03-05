from django.shortcuts import render
from django.views import View

from .forms import CheckoutForm
from core.contexts import get_base_context


class Checkout(View):
    template = 'checkout/checkout.html'

    def get(self, request):
        context = get_base_context(request)
        context['form'] = CheckoutForm()

        return render(request, self.template, context)
