from django.conf import settings
from .models import Order, OrderLineItem
from datetime import datetime


# The fields the order is expecting. Everything else is deleted
EXPECTED_FIELDS = [
    'bake_date',
    'customer_note',
    'delivery',
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


def create_order(checkout_data, cart):
    """
    Creates an order
    """
    bake_date = datetime.strptime(
        checkout_data['bake_date'],
        '%Y-%m-%d'
    )

    # Deleting any unknown keys in the input
    new_data = dict(checkout_data.copy())
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
    return order
