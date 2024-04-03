from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import NewsletterEmails

import os


# Used to supply links within emails
CURRENT_DOMAIN = 'development' if 'DEVELOPMENT' in os.environ else 'deployed'
SITE_DOMAIN = f"https://{settings.DOMAINS[CURRENT_DOMAIN]}"


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
    send_html_email(subject, body, email_to)


def send_newsletter(subject, body, discount_code=None):
    """
    Sends a newsletter to all active subscribers
    """
    subscribers = list(NewsletterEmails.objects.filter(
        is_active=True
    ))
    for subscriber in subscribers:
        send_html_email(subject, body, subscriber.email)
        if discount_code:
            subscriber.received_codes.add(discount_code)


def send_html_email(subject, body, email_to):
    """
    Sends an HTML version of the email, replacing the unsubscribe
    tag with an anchor
    """
    unsubscribe = f'{SITE_DOMAIN}/contact/newsletter_unsubscribe/{email_to}'
    # The regular text body
    body_text = body.replace('@UNSUBSCRIBE', f'Unsubscribe: {unsubscribe}')

    # The HTML body
    body_anchor = body.replace('\n', '<br>').replace(
        '@UNSUBSCRIBE',
        f"""<a href="{SITE_DOMAIN}/contact/newsletter_unsubscribe/{email_to}">
                <small>Unsubscribe from newsletter</small></a>"""
    )

    body_html = f"""
    <html>
        <head></head>
        <body>
            {body_anchor}
        </body
    </html>
    """
    send_mail(subject, body_text, settings.DEFAULT_FROM_EMAIL,
              [email_to], html_message=body_html)
