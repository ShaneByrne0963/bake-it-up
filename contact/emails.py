from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import NewsletterEmails

import os


# Used to supply links within emails
SITE_DOMAIN = f"https://{settings.DOMAINS[
    'development' if 'DEVELOPMENT' in os.environ else 'deployed'
]}"


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
        f'contact/emails/body/{template_name}.txt', {
            'site_domain': SITE_DOMAIN,
            'email_to': email_to,
            **kwargs
        }
    )
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
              [email_to])


def send_newsletter(subject, body, discount_code=None):
    """
    Sends a newsletter to all active subscribers
    """
    subscribers = list(NewsletterEmails.objects.filter(
        is_active=True
    ))
    for subscriber in subscribers:
        email = subscriber.email
        body_with_link = body.replace(
            '<a></a>',
            f'<a href="{SITE_DOMAIN}/contact/newsletter_unsubscribe/{email}"> \
                Unsubscribe from newsletter</a>'
        )
        send_mail(subject, body_with_link,
                  settings.DEFAULT_FROM_EMAIL,
                  [email])
        if discount_code:
            subscriber.received_codes.add(discount_code)
