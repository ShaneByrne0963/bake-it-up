from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from allauth.account.views import LoginView, SignupView
from allauth.account.forms import LoginForm, SignupForm

from core.contexts import get_base_context, handle_server_errors, \
                          get_products
from profiles.models import UserProfile


class Home(View):
    """
    View to bring the user to the home page
    """
    template = 'home/index.html'

    @handle_server_errors
    def get(self, request):
        context = get_base_context(request)
        best_products = get_products(request)[:4]
        context['best_products'] = best_products
        return render(request, self.template, context)


class CustomLogin(LoginView):
    """
    Allows the allauth login to be performed on all pages within
    the modal
    """
    @handle_server_errors
    def get(self, request):
        """
        Redirects the user to the home page, with the login modal
        appearing on page load
        """
        request.session['global_context'] = {
            'modal_show': 'login',
            'modal_load_fade': True
        }
        return redirect('home')

    @handle_server_errors
    def post(self, request):
        url_next = '/'
        if 'next' in request.POST:
            url_next = request.POST['next']
        email = request.POST['login']
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            login_next = super().post(request)

            # Custom login message
            if request.user.is_authenticated:
                login_message = ''
                user_fname = request.user.first_name
                if user_fname:
                    login_message = f'Welcome back, {user_fname}!'
                else:
                    login_message = f'Signed in as {email}'
                messages.success(request, login_message)

            # Allowing a different URL to be redirected to
            if 'login_custom_redirect' in request.POST:
                return redirect(request.POST['login_custom_redirect'])

            return login_next

        request.session['global_context'] = {
            'modal_show': 'login',
            'val_login': email,
            'modal_form_errors': login_form.errors.as_json(),
        }
        if 'remember' in request.POST:
            request.session['global_context']['val_remember'] = True

        return redirect(url_next)


class CustomSignup(SignupView):

    @handle_server_errors
    def get(self, request):
        """
        Redirects the user to the home page, with the signup modal
        appearing on page load
        """
        request.session['global_context'] = {
            'modal_show': 'signup',
            'modal_load_fade': True
        }
        return redirect('home')

    @handle_server_errors
    def post(self, request):
        email = request.POST['email']
        signup_form = SignupForm(request.POST)

        if signup_form.is_valid():
            next_url = super().post(request)

            # Adding the first and/or last name if specified
            try:
                user = User.objects.get(email=email)
                if 'first_name' in request.POST:
                    user.first_name = request.POST['first_name']
                if 'last_name' in request.POST:
                    user.last_name = request.POST['last_name']
                user.save()
                # Creating the profile for this user
                profile = UserProfile(
                    user=user
                )
                profile.save()
            except Exception:
                messages.error(
                    request,
                    "There was a problem creating your account. \
                    Please try again."
                )

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
    @handle_server_errors
    def get(self, request):
        request.session['global_context'] = {
            'modal_show': 'login',
            'modal_load_fade': 'True',
        }
        return redirect('home')


class PrivacyPolicy(View):
    template = 'home/privacy_policy.html'

    def get(self, request):
        context = get_base_context(request)
        return render(request, self.template, context)


# Error pages

def handler404(request):
    """404 page"""
    context = get_base_context(request)
    return render(request, '404.html', context)


def handler500(request):
    """500 page"""
    context = get_base_context(request)
    return render(request, '404.html', context)
