from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from core.contexts import get_base_context
from .forms import ProfileContactForm, ProfileBillingForm
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
                'profile_fname': {
                    'label': 'First Name',
                    'value': request.user.first_name,
                },
                'profile_lname': {
                    'label': 'Last Name',
                    'value': request.user.last_name,
                },
                'email': {
                    'label': 'Email Address',
                    'value': request.user.email,
                },
                'phone': {
                    'label': 'Phone Number',
                    'value': profile.saved_phone_number,
                },
            }
            billing_details = {
                'street_address1': {
                    'label': 'Street Address' + ' (Line 1)' \
                        if profile.saved_street_address2 else '',
                    'value': profile.saved_street_address1,
                },
                'street_address2': {
                    'label': 'Street Address (Line 2)',
                    'value': profile.saved_street_address2,
                },
                'town_or_city': {
                    'label': 'First Name',
                    'value': profile.saved_town_or_city,
                },
                'county': {
                    'label': 'First Name',
                    'value': profile.saved_county,
                },
                'postcode': {
                    'label': 'First Name',
                    'value': profile.saved_postcode,
                },
            }
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
            messages.warning(
                request,
                """Your account details are missing. Any data previously
                entered has been reset."""
            )
        except Exception as e:
            messages.error(
                request,
                f"""Sorry, but your profile cannot be accessed at the
                moment. Please try again later or contact us if the
                problem persists. {e}
                """
            )
            return redirect('home')

        # Checking if any details exist for each form
        contact_form = None
        has_contact_details = False
        for key in contact_details:
            if contact_details[key]['value']:
                has_contact_details = True
                context['contact_details'] = contact_details
                contact_form = ProfileContactForm(
                    {key: value['value'] for key, value in contact_details.items()}
                )
                break
        billing_form = None
        has_billing_details = False
        for key in billing_details:
            if billing_details[key]['value']:
                has_billing_details = True
                context['billing_details'] = billing_details
                billing_form = ProfileBillingForm(
                    {key: value['value'] for key, value in billing_details.items()}
                )
                break
        
        context['has_contact_details'] = has_contact_details
        context['has_billing_details'] = has_billing_details

        if contact_form is None:
            contact_form = ProfileContactForm()
        if billing_form is None:
            billing_form = ProfileBillingForm()
        context['contact_form'] = contact_form
        context['billing_form'] = billing_form

        return render(request, self.template, context)