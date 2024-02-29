def add_to_cart(product, cart):

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
