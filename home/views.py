from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from allauth.account.views import LoginView, SignupView
from allauth.account.forms import LoginForm, SignupForm

from core.contexts import get_base_context


class Home(View):
    """
    View to bring the user to the home page
    """
    template = 'home/index.html'

    def get(self, request):
        context = get_base_context(request)
        return render(request, self.template, context)


class CustomLogin(LoginView):
    """
    Allows the allauth login to be performed on all pages within
    the modal
    """
    def post(self, request):
        url_next = request.POST['next']
        username = request.POST['login']
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            return super().post(request)

        request.session['global_context'] = {
            'modal_show': 'login',
            'val_login': username,
            'modal_form_errors': login_form.errors.as_json(),
        }
        if 'remember' in request.POST:
            request.session['global_context']['val_remember'] = True

        return redirect(url_next)


class CustomSignup(SignupView):

    def post(self, request):
        email = request.POST['email']
        signup_form = SignupForm(request.POST)

        if signup_form.is_valid():
            next_url = super().post(request)

            # Adding the first and/or last name if specified
            user = User.objects.get(email=email)
            if user:
                if 'first_name' in request.POST:
                    user.first_name = request.POST['first_name']
                if 'last_name' in request.POST:
                    user.last_name = request.POST['last_name']
                user.save()

            return next_url

        request.session['global_context'] = {
            'modal_show': 'signup',
            'val_first_name': request.POST['first_name'],
            'val_last_name': request.POST['last_name'],
            'val_email': email,
            'modal_form_errors': signup_form.errors.as_json(),
        }
        return redirect(request.POST['next'])


class EmailConfirmed(View):
    """
    Redirects the user to the home page after the user verifies
    their email, and causes the login modal to appear
    """
    def get(self, request):
        request.session['global_context'] = {
            'modal_show': 'login',
            'modal_load_fade': 'True',
        }
        return redirect('home')


class TestToast(View):

    def get(self, request, toast_type):
        message_type = None
        message_body = ''

        if toast_type == 'success':
            message_body = 'This is a success toast'
            message_type = messages.SUCCESS
        elif toast_type == 'info':
            message_body = 'This is an info toast'
            message_type = messages.INFO
        elif toast_type == 'warning':
            message_body = 'This is a warning toast'
            message_type = messages.WARNING
        else:
            message_body = 'This is an error toast'
            message_type = messages.ERROR
        
        messages.add_message(request, message_type, message_body)
        return redirect('home')
