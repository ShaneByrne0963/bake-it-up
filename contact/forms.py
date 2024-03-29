from django import forms
from .models import CustomerMessage, NewsletterEmails


class CustomerMessageForm(forms.ModelForm):

    class Meta:
        model = CustomerMessage
        fields = ('full_name', 'email', 'title', 'message')


class NewsletterSignupForm(forms.ModelForm):

    class Meta:
        model = NewsletterEmails
        fields = ('email',)
