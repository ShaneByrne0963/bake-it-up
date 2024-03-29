from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

import os


def send_template_email(template_name, email_to, **kwargs):
    """
    Sends an email based on a template found in
    templates/checkout/emails/
    """
    subject = render_to_string(
        f'contact/emails/subject/{template_name}.txt',
        { **kwargs }
    )
    body = render_to_string(
        f'contact/emails/body/{template_name}.txt',
        { **kwargs }
    )
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
              [email_to])
