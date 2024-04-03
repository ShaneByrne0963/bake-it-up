from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Order, OrderLineItem
from profiles.models import UserProfile
from contact.models import NewsletterEmails

from datetime import datetime


# The fields the order is expecting. Everything else is deleted
EXPECTED_FIELDS = [
    'bake_date',
    'customer_note',
    'delivery',
    'discount',
    'full_name',
    'email',
    'phone_number',
    'street_address1',
    'street_address2',
    'town_or_city',
    'county',
    'postcode',
    'stripe_pid',
    'delivery_line1',
    'delivery_line2',
    'delivery_city',
    'delivery_county',
    'delivery_postcode'
]


def create_order(checkout_data, cart, save_info=False, user=None):
    """
    Creates an order
    """
    bake_date = datetime.strptime(
        checkout_data['bake_date'],
        '%Y-%m-%d'
    )
    new_data = dict(checkout_data.copy())

    # Deleting any unknown keys in the input
    for key, value in checkout_data.items():
        if isinstance(value, list):
            value = value[0]
        if key == 'name':
            new_data['full_name'] = value
        if key == 'phone':
            new_data['phone_number'] = value
        if key == 'pid':
            new_data['stripe_pid'] = value

        if key in EXPECTED_FIELDS:
            # Checkbox values
            if value == 'on':
                new_data[key] = True
            else:
                new_data[key] = value
        else:
            del new_data[key]

    if 'delivery' not in new_data:
        new_data['delivery'] = False
    new_data['bake_date'] = bake_date
    new_data['profile'] = UserProfile.objects.get(user=user)

    # Calculating the delivery cost
    if new_data['delivery']:
        delivery_county = None
        if 'delivery_county' in new_data \
                and new_data['delivery_county']:
            delivery_county = new_data['delivery_county']
        else:
            delivery_county = new_data['county']
        delivery_cost = settings.COUNTY_DELIVERY_COSTS[delivery_county]
        new_data['delivery_cost'] = delivery_cost

    order = Order.objects.create(**new_data)

    for item in cart:
        # Getting custom properties, with None as a default
        properties = {
            'shape': None,
            'size': None,
            'contents': None,
            'type': None,
            'color': None,
            'icing': None,
            'decoration': None,
            'text': None
        }
        for prop in item['prop_list']:
            properties[prop['name']] = prop['answer']

        line_item = OrderLineItem(
            order=order,
            product_name=item['name'],
            quantity=item['quantity'],
            prop_shape=properties['shape'],
            prop_size=properties['size'],
            prop_contents=properties['contents'],
            prop_type=properties['type'],
            prop_color=properties['color'],
            prop_icing=properties['icing'],
            prop_decoration=properties['decoration'],
            prop_text=properties['text'],
        )
        line_item.save()
    
    # Saving the user's profile information
    if save_info and user:
        update_user_profile(new_data, user)
    
    # Sending a confirmation email
    from_email = settings.DEFAULT_FROM_EMAIL
    subject = render_to_string(
        'checkout/confirmation_emails/email_subject.txt',
        { 'order': order }
    )
    body = render_to_string(
        'checkout/confirmation_emails/email_body.txt',
        { 'order': order, 'contact_email': from_email }
    )
    send_mail(subject, body, from_email, [checkout_data['email']])

    return order


def update_user_profile(checkout_data, user):
    """
    Saves the billing details to the user's profile
    """
    user_profile = None
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=user)
    except Exception as e:
        return
    user_profile.saved_phone_number = checkout_data['phone_number']
    user_profile.saved_street_address1 = checkout_data['street_address1']
    user_profile.saved_street_address2 = checkout_data['street_address2']
    user_profile.saved_town_or_city = checkout_data['town_or_city']
    user_profile.saved_county = checkout_data['county']
    user_profile.saved_postcode = checkout_data['postcode']
    user_profile.save()
