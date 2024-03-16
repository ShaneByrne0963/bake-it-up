from django.conf import settings
from products.forms import get_default_label
from core.shortcuts import convert_24_hour_to_12

from datetime import datetime, timedelta


def add_to_cart(product, cart):
    """
    Adds an item to the session storage cart, combining
    identical products with the same properties.
    The "product" object must contain keys "name" and
    "quantity". Everything else is optional
    """
    # Error handling
    if not isinstance(product, dict):
        raise TypeError("product must be of type dict")
    if not isinstance(cart, list):
        raise TypeError("cart must be of type list")
    if 'name' not in product:
        raise KeyError('No "name" key found in product')
    if 'quantity' not in product:
        raise KeyError('No "quantity" key found in product')
    if not isinstance(product['name'], str):
        raise TypeError('"name" value in product must be a string')
    if not isinstance(product['quantity'], int):
        raise TypeError('"quantity" value in product must be an \
        integer')
    if product['quantity'] <= 0:
        raise ValueError('"quantity" value in product must be \
        greater than zero')
    
    is_in_cart = False
    for cart_product in cart:

        # Comparing the products without their quantity
        product_copy = product.copy()
        cart_copy = cart_product.copy()
        del product_copy['quantity']
        del cart_copy['quantity']

        if product_copy == cart_copy:
            cart_product['quantity'] += product['quantity']
            is_in_cart = True
            break

    if not is_in_cart:
        cart.append(product)
    return cart


def get_properties_from_dict(product, properties):
    """
    Gets a list of all properties of a product
    specified in the properties dict
    """
    list_of_properties = []
    for key, value in properties.items():
        if 'prop_' not in key:
            continue
        prop_details = getattr(product, key)
        name = key.replace('prop_', '')
        label = ''
        answer = value

        if name == 'text':
            prop_dict = {
                'name': 'text',
                'label': 'Text',
                'value': value,
                'answer': answer
            }
            list_of_properties.append(prop_dict)
            continue

        # Specifying the label to be shown in the cart
        if 'label' in prop_details:
            label = prop_details['label']
        elif value != 'on':
            # Checkbox inputs with no set label will just
            # display the answer
            label = get_default_label(name)

        # Finding the chosen answer from the model, to
        # prevent users from editing the answer
        if value.isdigit():
            value = int(value)
            answer = prop_details['answers'][value]
        else:
            if isinstance(prop_details['answers'], list):
                answer = prop_details['answers'][0]
            else:
                answer = prop_details['answers']

        prop_dict = {
            'name': name,
            'label': label,
            'value': value,
            'answer': answer
        }
        list_of_properties.append(prop_dict)

    return list_of_properties


def has_reached_cutoff_time(current_datetime=None):
    """
    Returns true if the current time has passed the cutoff time
    to bake the products the next day
    """
    if not current_datetime:
        current_datetime = datetime.now()

    current_time = datetime.time(current_datetime).strftime('%H:%M')
    current_hour = current_time.split(':')[0]
    current_hour = int(current_hour)

    return current_hour >= settings.NEXT_DAY_CUTOFF_TIME
