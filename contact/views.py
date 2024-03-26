from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.views.decorators.http import require_POST
from django.contrib import messages

from core.contexts import get_base_context
from .forms import CustomerMessageForm
from .models import CustomerMessage


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


class ViewMessages(View):
    template = 'contact/view_messages.html'

    def get(self, request):
        context = get_base_context(request)
        unopen_messages = CustomerMessage.objects.filter(
            opened=False
        ).order_by('-date_created')

        open_messages = CustomerMessage.objects.filter(
            opened=True
        ).order_by('-date_created')

        context['unopen_messages'] = unopen_messages
        context['open_messages'] = open_messages

        return render(request, self.template, context)


class DeleteMessage(View):

    def post(self, request, message_id):
        message = CustomerMessage.objects.get(id=message_id)
        message.delete()
        messages.success(
            request,
            'Message successfully deleted'
        )
        return redirect('view_messages')


class NewsletterSignup(View):

    def post(self, request):
        pass


@require_POST
def open_message(request, message_id):
    """
    Tells the server that an admin has opened a message
    """
    try:
        message = CustomerMessage.objects.get(id=message_id)
        message.opened = True
        message.save()

        # Getting how many unread messages are left
        num_messages = CustomerMessage.objects.filter(
            opened=False
        ).count()
    
        return HttpResponse(content=num_messages, status=200)
    except Exception as e:
        return HttpResponse(content=e, status=400)
