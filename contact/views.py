from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.views.decorators.http import require_POST
from django.contrib import messages

from core.contexts import get_base_context, handle_server_errors, \
                          admin_action
from .forms import CustomerMessageForm, NewsletterSignupForm
from .models import CustomerMessage, NewsletterEmails, DiscountCode
from .emails import send_template_email, send_newsletter

from datetime import date


class StoreContact(View):
    template = 'contact/store_contact.html'

    @handle_server_errors
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

    @handle_server_errors
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

    @handle_server_errors
    @admin_action
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


class DeleteMessage(View):

    @handle_server_errors
    @admin_action
    def post(self, request, message_id):
        message = CustomerMessage.objects.get(id=message_id)
        message.delete()
        messages.success(
            request,
            'Message successfully deleted'
        )
        return redirect('view_messages')


class NewsletterSignup(View):

    @handle_server_errors
    def post(self, request):
        url_next = request.POST.get('next', '')
        # Allows the page to focus on the input on page reload
        focus = '#newsletter-email'
        if 'email' not in request.POST:
            request.session['global_context'] = {
                'newsletter_error': 'Please enter an email address'
            }
            return redirect(f'{url_next}{focus}')
        email = request.POST['email']

        # Checking if the email already exists in the database
        response = NewsletterSignup.subscribe_email(email)
        if response == 'Email already active':
            request.session['global_context'] = {
                'newsletter_error': """
                    This email is already subscribed to the
                    newsletter."""
            }
            return redirect(f'{url_next}{focus}')
        elif response == 'New subscription':
            messages.success(
                request,
                'You have signed up for our newsletter!'
            )
        elif response == 'Subscription reactivated':
            messages.success(
                request,
                'Your newsletter subscription has been reactivated!'
            )
        else:
            messages.error(
                request,
                f"An unexpected error occurred. {response}"
            )
        return redirect(url_next)
    
    @staticmethod
    def subscribe_email(email):
        """
        Signs the email up to the newsletter, and returns one of
        the following responses:
        - Email already active
        - New subscription
        - Subscription reactivated
        - Any other response is a caught error
        """
        # Checking if the email already exists in the database
        try:
            newsletter = NewsletterEmails.objects.get(email=email)
            if newsletter.is_active:
                return 'Email already active'
            else:
                newsletter.is_active = True
                newsletter.save()
                send_template_email('resubscribe', email)

                return 'Subscription reactivated'
        except NewsletterEmails.DoesNotExist:
            # Creating a new subscription
            newsletter_form = NewsletterSignupForm({'email': email})
            if newsletter_form.is_valid():
                newsletter_email = newsletter_form.save()
                send_template_email('subscribe', email)

                # Applying the BAKEITUPNEWS10 code for new subscribers
                discount_code = DiscountCode.objects.get(
                    code_name='BAKEITUPNEWS10'
                )
                newsletter_email.received_codes.add(discount_code)
                newsletter_email.save()

                return 'New subscription'

        except Exception as e:
            return e


class SendNewsletter(View):
    template = 'contact/send_newsletter.html'

    @handle_server_errors
    @admin_action
    def get(self, request):
        context = get_base_context(request)
        context['today'] = date.today()
        
        return render(request, self.template, context)
    
    @handle_server_errors
    @admin_action
    def post(self, request):
        subject = request.POST['subject']
        body = request.POST['newsletter_format']
        new_discount = None

        # Creating the discount code
        if 'has_discount' in request.POST:
            is_percentage = (request.POST['is_percentage'] == 'true')
            min_spending = 0
            if 'has_minimum_spend' in request.POST:
                min_spending = request.POST['min_spending']

            new_discount = DiscountCode(
                code_name=request.POST['code_name'],
                discount_value=request.POST['discount_value'],
                is_percentage=is_percentage,
                min_spending=min_spending
            )
            new_discount.save()
        send_newsletter(subject, body, new_discount)
        messages.success(request, "Your newsletter has been sent!")
        return redirect('send_newsletter')


@require_POST
def check_code_name(request):
    """
    Checks if the code name already exists, as each name must
    be unique
    """
    try:
        DiscountCode.objects.get(
            code_name=request.POST['code_name']
        )
        return HttpResponse(
            content='That code name already exists.',
            status=400
        )
    except DiscountCode.DoesNotExist:
        return HttpResponse(content='Success', status=200)
    except Exception as e:
        return HttpResponse(content=e, status=400)


class NewsletterUnsubscribe(View):
    template = 'contact/newsletter_unsubscribe.html'

    @handle_server_errors
    def get(self, request, email):
        context = get_base_context(request)
        context['unsubscribe_email'] = email

        return render(request, self.template, context)
    
    @handle_server_errors
    def post(self, request, email):
        newsletter_email = None
        try:
            newsletter_email = NewsletterEmails.objects.get(
                email=email
            )
        except NewsletterEmails.DoesNotExist:
            # It doesn't matter if the email doesn't exist in the
            # database, as we want to stop the newsletters anyway
            pass
        else:
            newsletter_email.is_active = False
            newsletter_email.save()
        finally:
            messages.success(
                request,
                "You have unsubscribed from our newsletter"
            )
            return redirect('home')
