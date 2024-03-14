from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from core.contexts import get_base_context
from .models import UserProfile


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

        # Getting the user profile, or creating one if none exists
        try:
            profile = UserProfile.objects.get(user=request.user)
            contact_details = {
                'saved_first_name': request.user.first_name,
                'saved_last_name': request.user.last_name,
                'saved_phone_number': profile.saved_phone_number,
            }
            billing_details = {
                'saved_street_address1': profile.saved_street_address1,
                'saved_street_address2': profile.saved_street_address2,
                'saved_town_or_city': profile.saved_town_or_city,
                'saved_county': profile.saved_county,
                'saved_postcode': profile.saved_postcode,
            }
            context['contact_details'] = contact_details
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
            messages.warning(
                request,
                """Your account details are missing. Any data previously
                entered has been reset."""
            )

        return render(request, self.template, context)