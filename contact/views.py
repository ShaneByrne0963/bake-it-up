from django.shortcuts import render
from django.views import View

from core.contexts import get_base_context
from .forms import CustomerMessageForm


class StoreContact(View):
    template = 'contact/store_contact.html'

    def get(self, request):
        context = get_base_context(request)
        contact_form = CustomerMessageForm()
        context['contact_form'] = contact_form

        return render(request, self.template, context)
