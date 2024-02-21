from django.shortcuts import render, redirect
from allauth.account.views import LoginView, SignupView
from allauth.account.forms import LoginForm, SignupForm
from django.views import View
from django.http import HttpResponse
from core.contexts import get_base_context
from django.contrib.auth import authenticate


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
        url_next = request.POST['next']
        username = request.POST['username']
        email = request.POST['email']
        signup_form = SignupForm(request.POST)

        if signup_form.is_valid():
            return super().post(request)

        request.session['global_context'] = {
            'modal_show': 'signup',
            'val_username': username,
            'val_email': email,
            'modal_form_errors': signup_form.errors.as_json(),
        }
        return redirect(url_next)


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
