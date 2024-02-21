from django.shortcuts import render, redirect
from allauth.account.views import LoginView
from allauth.account.forms import LoginForm
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
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=username, password=password)
            if user is not None:
                super().post(request)

        return redirect(url_next)
