from .models import Order, OrderLineItem
from datetime import datetime


# region checkout_data keys
"""
checkout_data = {
    'name',
    'email',
    'phone',
    'street_address1',
    'street_address2',
    'town_or_city',
    'county',
    'postcode',
    'pid'
}
"""
# endregion

def create_order(checkout_data, cart):
    """
    Creates an order
    """
    bake_date = datetime.strptime(
        checkout_data['bake_date'],
        '%Y-%m-%d'
    )
    print(checkout_data['bake_date'])
    print(bake_date)
    order = Order(
        bake_date=checkout_data['bake_date'],
        customer_note=checkout_data['customer_note'],
        full_name=checkout_data['name'],
        email=checkout_data['email'],
        phone_number=checkout_data['phone'],
        street_address1=checkout_data['street_address1'],
        street_address2=checkout_data['street_address2'],
        town_or_city=checkout_data['town_or_city'],
        county=checkout_data['county'],
        postcode=checkout_data['postcode'],
        stripe_pid=checkout_data['pid']
    )
    order.save()

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
