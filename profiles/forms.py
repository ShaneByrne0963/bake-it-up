from django import forms

from core.constants import COUNTY_CHOICES

class ProfileContactForm(forms.Form):

    profile_fname = forms.CharField(
        label="First Name",
        max_length=30,
        required=False
    )
    profile_lname = forms.CharField(
        label="Last Name",
        max_length=30,
        required=False
    )
    email = forms.EmailField(
        label="Email Address",
        max_length=320,
        required=False
    )
    phone = forms.CharField(
        label="Phone Number",
        max_length=20,
        required=False
    )


class ProfileBillingForm(forms.Form):

    street_address1 = forms.CharField(
        label="Address Line 1",
        max_length=60,
        required=False
    )
    street_address2 = forms.CharField(
        label="Address Line 2",
        max_length=60,
        required=False
    )
    town_or_city = forms.CharField(
        label="Town/City",
        max_length=60,
        required=False
    )
    county = forms.ChoiceField(
        choices=COUNTY_CHOICES,
        required=False
    )
    postcode = forms.CharField(
        label="Postal Code",
        max_length=10,
        required=False
    )
