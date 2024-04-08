from django import forms

from core.constants import COUNTY_CHOICES

PROFILE_FORM_LABELS = {
    'profile_fname': 'First Name',
    'profile_lname': 'Last Name',
    'email': 'Email Address',
    'phone': 'Phone Number',
    'street_address1': 'Street Address',
    'street_address2': 'Street Address (Line 2)',
    'town_or_city': 'Town/City',
    'county': 'County',
    'postcode': 'Postal Code'
}

# Allows users to clear their county information
NO_COUNTY_OPTION = (
    ('', 'No Default County'),
)

REQUIRED_FIELDS = ('email',)


class BaseProfileForm(forms.Form):
    """
    Applies the label to both forms, and sets all
    fields to not required
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.fields.items():
            self.fields[key].label = PROFILE_FORM_LABELS[key]
            classes = ''

            # Allow commas in the street address inputs
            if 'street_address' in key:
                self.fields[key].widget.attrs['class'] = 'allow-commas'

            if key not in REQUIRED_FIELDS:
                self.fields[key].required = False    


class ProfileContactForm(BaseProfileForm):

    profile_fname = forms.CharField(max_length=30)
    profile_lname = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=320, required=True)
    phone = forms.CharField(max_length=20)


class ProfileBillingForm(BaseProfileForm):

    street_address1 = forms.CharField(max_length=60)
    street_address2 = forms.CharField(max_length=60)
    town_or_city = forms.CharField(max_length=60)
    county = forms.ChoiceField(
        choices=(NO_COUNTY_OPTION + COUNTY_CHOICES)
    )
    postcode = forms.CharField(max_length=10)
