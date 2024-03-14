from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from core.contexts import get_base_context
from .forms import ProfileContactForm, ProfileBillingForm, PROFILE_FORM_LABELS
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

        contact_details = {
            'profile_fname': request.user.first_name,
            'profile_lname': request.user.last_name,
            'email': request.user.email,
            'phone': '',
        }
        billing_details = {
            'street_address1': '',
            'street_address2': '',
            'town_or_city': '',
            'county': '',
            'postcode': '',
        }

        # Getting the user profile, or creating one if none exists
        try:
            profile = UserProfile.objects.get(user=request.user)
            contact_details['phone'] = profile.saved_phone_number
            billing_details['street_address1'] = profile.saved_street_address1
            billing_details['street_address2'] = profile.saved_street_address2
            billing_details['town_or_city'] = profile.saved_town_or_city
            billing_details['county'] = profile.saved_county
            billing_details['postcode'] = profile.saved_postcode

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
            if contact_details[key]:
                has_contact_details = True
                context['contact_details'] = {
                    key: {
                        'label': PROFILE_FORM_LABELS[key],
                        'value': value
                    } for key, value in contact_details.items()
                }
                contact_form = ProfileContactForm(contact_details)
                break
        billing_form = None
        has_billing_details = False
        for key in billing_details:
            if billing_details[key]:
                has_billing_details = True
                context['billing_details'] = {
                    key: {
                        'label': PROFILE_FORM_LABELS[key],
                        'value': value
                    } for key, value in billing_details.items()
                }
                billing_form = ProfileBillingForm(billing_details)
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