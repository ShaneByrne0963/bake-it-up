from django import forms
from django.conf import settings

from core.constants import COUNTY_CHOICES


class ContactDetailsForm(forms.Form):

    first_name = forms.CharField(
        label="First Name",
        max_length=30,
        required=True
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=30,
        required=True
    )
    email = forms.EmailField(
        label="Email Address",
        max_length=320,
        required=True
    )
    phone = forms.CharField(
        label="Phone Number",
        max_length=20,
        required=True
    )


class BillingDetailsForm(forms.Form):

    street_address1 = forms.CharField(
        label="Address Line 1",
        max_length=60,
        required=True
    )
    street_address2 = forms.CharField(
        label="Address Line 2",
        max_length=60,
        required=False
    )
    town_or_city = forms.CharField(
        label="Town/City",
        max_length=60,
        required=True
    )
    county = forms.ChoiceField(
        choices=COUNTY_CHOICES
    )
    postcode = forms.CharField(
        label="Postal Code",
        max_length=10
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['street_address1'].widget.attrs['class'] = 'allow-commas'
        self.fields['street_address2'].widget.attrs['class'] = 'allow-commas'
