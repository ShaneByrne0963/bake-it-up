from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.views import View
from home.views import CustomLogin
from allauth.account.admin import EmailAddress
from allauth.account.utils import send_email_confirmation

from core.contexts import get_base_context, add_field_error
from .forms import ProfileContactForm, ProfileBillingForm, PROFILE_FORM_LABELS
from .models import UserProfile
from checkout.models import Order

from datetime import datetime


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
        profile = None

        # The default profile details
        contact_details = {
            'profile_fname': request.user.first_name,
            'profile_lname': request.user.last_name,
            'email': request.user.email,
        }
        billing_details = {}

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
                break
    
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
                break
        
        context['has_contact_details'] = has_contact_details
        context['has_billing_details'] = has_billing_details

        # Retrieving any previously entered information
        if 'invalid_contact_details' in context:
            contact_details.update({
                'profile_fname': context['val_profile_fname'],
                'profile_lname': context['val_profile_lname'],
                'email': context['val_profile_email'],
                'phone': context['val_profile_phone']
            })
        if 'invalid_billing_details' in context:
            contact_details.update({
                'street_address1': context['val_profile_line1'],
                'street_address2': context['val_profile_line2'],
                'town_or_city': context['val_profile_city'],
                'county': context['val_profile_county'],
                'postcode': context['val_profile_postcode']
            })

        contact_form = ProfileContactForm(contact_details)
        billing_form = ProfileBillingForm(billing_details)
        context['contact_form'] = contact_form
        context['billing_form'] = billing_form

        # Getting the user's list of previous orders
        orders = Order.objects.filter(
            profile=profile
        ).order_by('-order_date')
        context['orders'] = orders

        return render(request, self.template, context)

    def post(self, request):
        """
        Updates the user's information
        """
        profile = UserProfile.objects.get(user=request.user)
        form = None
        form_type = request.POST.get('form_type', '')
        update_success = False
        form_invalid = False
        email_changed = None
        verified_user = None

        # The contact details form
        if form_type == 'contact':
            update_success = True
            new_fname = request.POST.get('profile_fname', '')
            new_lname = request.POST.get('profile_lname', '')
            new_phone = request.POST.get('phone', '')

            # Password verification for changing emails
            new_email = request.POST.get('email', '')
            old_email = request.user.email
            if new_email != old_email:
                if 'password' not in request.POST:
                    messages.error(
                        request,
                        """Access denied. No password was given for
                        email update"""
                    )
                    return redirect('account_settings')

                verified_user = authenticate(
                    email=request.user.email,
                    password=request.POST['password']
                )
                if verified_user is None:
                    update_success = False
                    # Creating an error message in the modal
                    form_error = add_field_error(
                        'verify-password',
                        "The password you have entered is incorrect"
                    )
                    # Setting up the modal to display on the next page
                    request.session['global_context'] = {
                        'modal_show': 'verify-password',
                        'modal_form_type': 'update_email',
                        'modal_form_errors': form_error,
                    }
            # Form Validation
            if update_success:
                update_success = False
                request.session['global_context'] = {}
                form = ProfileContactForm(request.POST)
                if form.is_valid():
                    request.user.first_name = new_fname
                    request.user.last_name = new_lname
                    request.user.email = new_email
                    profile.saved_phone_number = new_phone
                    update_success = True
                    request.user.save()
                    if old_email != new_email:
                        email_changed = new_email
                else:
                    form_invalid = True

            if not update_success:
                request.session['global_context'].update({
                    'invalid_contact_details': True,
                    'val_profile_fname': new_fname,
                    'val_profile_lname': new_lname,
                    'val_profile_email': new_email,
                    'val_profile_phone': new_phone
                })
    
        # The billing details form
        elif form_type == 'billing':
            new_line1 = request.POST.get('street_address1', '')
            new_line2 = request.POST.get('street_address2', '')
            new_city = request.POST.get('town_or_city', '')
            new_county = request.POST.get('county', '')
            new_postcode = request.POST.get('postcode', '')

            form = ProfileBillingForm(request.POST)
            if form.is_valid():
                profile.saved_street_address1 = new_line1
                profile.saved_street_address2 = new_line2
                profile.saved_town_or_city = new_city
                profile.saved_county = new_county
                profile.saved_postcode = new_postcode
                update_success = True
            else:
                form_invalid = True
                request.session['global_context'] = {
                    'invalid_billing_details': True,
                    'val_profile_line1': new_line1,
                    'val_profile_line2': new_line2,
                    'val_profile_city': new_city,
                    'val_profile_county': new_county,
                    'val_profile_postcode': new_postcode
                }
        else:
            messages.error(request, 'Unknown form received')

        if update_success:
            profile.save()
            messages.success(
                request,
                "Your profile has been updated!"
            )
        elif form_invalid:
            messages.error(
                request,
                """Your information was invalid. 
                Please check your details"""
            )

        # New email authentication
        if email_changed:
            try:
                email_address = EmailAddress.objects.get(
                    user=request.user
                )
                email_address.delete()
            except EmailAddress.DoesNotExist:
                pass
            send_email_confirmation(request, request.user,
                                    email_changed)
            logout(request)
            return redirect('/accounts/confirm-email/')
        return redirect('account_settings')


class OrderDetails(View):
    template = 'profiles/order_details.html'

    def get(self, request, order_no):
        context = get_base_context(request)
        order = get_object_or_404(Order, order_number=order_no)
        context['order'] = order

        return render(request, self.template, context)


class DeleteAccount(View):

    def post(self, request):
        if 'password' not in request.POST:
            messages.error(
                request,
                """Access denied. No password was given for
                account deletion"""
            )
            return redirect('account_settings')

        verified_user = authenticate(
            email=request.user.email,
            password=request.POST['password']
        )
        if verified_user is None:
            # Creating an error message in the modal
            form_error = add_field_error(
                'verify-password',
                "The password you have entered is incorrect"
            )
            # Setting up the modal to display on the next page
            request.session['global_context'] = {
                'modal_show': 'verify-password',
                'modal_form_type': 'delete_account',
                'modal_form_errors': form_error,
            }
            return redirect('account_settings')
        else:
            verified_user.delete()
            messages.success(
                request,
                "Your account has been successfully deleted"
            )
            return redirect('home')
