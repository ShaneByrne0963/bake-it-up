from products.forms import get_default_label


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
