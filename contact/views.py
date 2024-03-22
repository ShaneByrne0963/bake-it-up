from django.shortcuts import render
from django.views import View

from core.contexts import get_base_context


class StoreContact(View):
    template = 'contact/store_contact.html'

    def get(self, request):
        context = get_base_context(request)

        return render(request, self.template, context)