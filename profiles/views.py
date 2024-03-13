from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from core.contexts import get_base_context


class AccountSettings(View):
    """
    A view to take the user to their account settings
    """
    template = 'profiles/account_settings.html'

    def get(self, request):
        # Making the login modal appear if the user isn't logged in
        if not request.user.is_authenticated:
            messages.error(
                request,
                'You must be logged in to view your account'
            )
            request.session['global_context'] = {
                'modal_show': 'login',
                'modal_load_fade': True,
                'login_custom_redirect': 'account_settings'
            }
            return redirect('home')

        context = get_base_context(request)
        return render(request, self.template, context)