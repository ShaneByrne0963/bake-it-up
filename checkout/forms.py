from django import forms

# A list of all counties for the select field
COUNTY_CHOICES = (
    ('Antrim', 'Antrim'),
    ('Armagh', 'Armagh'),
    ('Carlow', 'Carlow'),
    ('Cavan', 'Cavan'),
    ('Clare', 'Clare'),
    ('Cork', 'Cork'),
    ('Derry', 'Derry'),
    ('Donegal', 'Donegal'),
    ('Down', 'Down'),
    ('Dublin', 'Dublin'),
    ('Fermanagh', 'Fermanagh'),
    ('Galway', 'Galway'),
    ('Kerry', 'Kerry'),
    ('Kildare', 'Kildare'),
    ('Kilkenny', 'Kilkenny'),
    ('Laois', 'Laois'),
    ('Leitrim', 'Leitrim'),
    ('Limerick', 'Limerick'),
    ('Longford', 'Longford'),
    ('Louth', 'Louth'),
    ('Mayo', 'Mayo'),
    ('Meath', 'Meath'),
    ('Monaghan', 'Monaghan'),
    ('Offaly', 'Offaly'),
    ('Roscommon', 'Roscommon'),
    ('Sligo', 'Sligo'),
    ('Tipperary', 'Tipperary'),
    ('Tyrone', 'Tyrone'),
    ('Waterford', 'Waterford'),
    ('Westmeath', 'Westmeath'),
    ('Wexford', 'Wexford'),
    ('Wicklow', 'Wicklow'),
)

class CheckoutForm(forms.Form):

    name = forms.CharField(
        label="Name/Company Name",
        max_length=70,
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
    street_address1 = forms.CharField(
        label="Address Line 1",
        max_length=60,
        required=True
    )
    street_address2 = forms.CharField(
        label="Address Line 2",
        max_length=60
    )
    town_or_city = forms.CharField(
        label="Town/City",
        max_length=60
    )
    county = forms.ChoiceField(
        choices=COUNTY_CHOICES
    )
