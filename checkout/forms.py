from django import forms


class CheckoutForm(forms.Form):

    name = forms.CharField(label="Name/Company Name",
                           max_length=70,
                           required=True)
    email = forms.EmailField(label="Email Address",
                             max_length=320,
                             required=True)
    phone = forms.CharField(label="Phone Number",
                            max_length=20,
                            required=True)
    street_address1 = forms.CharField()
