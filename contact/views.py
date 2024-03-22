from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from core.contexts import get_base_context
from .forms import CustomerMessageForm


class StoreContact(View):
    template = 'contact/store_contact.html'

    def get(self, request):
        context = get_base_context(request)

        # Get the user's name and email
        user_info = {}
        if request.user.is_authenticated:
            user_info['email'] = request.user.email
            if request.user.first_name:
                full_name = request.user.first_name
                if request.user.last_name:
                    full_name += f' {request.user.last_name}'
                user_info['full_name'] = full_name

        contact_form = CustomerMessageForm(initial=user_info)
        context['contact_form'] = contact_form

        return render(request, self.template, context)
    
    def post(self, request):
        """
        Sends the customer message
        """
        contact_form = CustomerMessageForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, "Your message has been sent! \
                We will get back to you shortly.")
            return redirect('home')
        else:
            messages.error(request, "Your contact details are invalid. \
                Please double check your details and try again.")
            context = get_base_context(request)
            context['contact_form'] = contact_form
            return render(request, self.template, context)
