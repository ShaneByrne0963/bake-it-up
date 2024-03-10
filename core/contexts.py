from django.shortcuts import get_object_or_404

from products.models import BreadProduct, PastryProduct
from .shortcuts import price_as_float


# region List of Available Context Keys for global_context
"""
{
    'modal_show' {String}: Shows the modal on page load if
        exists. The string value indicates the form to be
        displayed in the modal, if any
    
    'modal_load_fade' {Truthy Expression}: Allows the modal fade
        animation on page load

    'modal_form_errors' {JSON}: A list of errors to be
        displayed in a modal form

    val_login {String}: The prefilled value for the login username

    val_remember {Truthy Expression}: Checks the login "Remember Me"
        checkbox
    
    val_username {String}: The prefilled value for the signup username

    val_email {String}: The prefilled value for the signup email address

    val_note {String}: The prefilled value for the user's note in
        the cart
    
    cutoff_reached {Truthy Expression}: If true, displays an error
        message in the cart that the user has reached the cutoff
        time for next day bake date
}
"""
# endregion

def get_base_context(request):
    """
    Returns the context required for the base template to function
    """
    # Getting any persistent context from the previous page
    context = request.session.pop('global_context', {})

    # Getting the cart total
    if 'cart_total' in request.session \
            and request.session['cart_total'] > 0:
        cart_total = request.session['cart_total']

        parsed_total = price_as_float(cart_total)
        context['cart_total'] = parsed_total

    return context


def get_cart_context(request):
    """
    Returns the base context, along with a list of products in the
    shopping cart
    """
    context = get_base_context(request)
    cart = request.session.get('cart', [])
    cart_products = []
    
    for item in cart:
        product = get_product_by_name(item['name'])
        quantity = int(item['quantity'])
        price = price_as_float(item['price'])
        prop_list = item['prop_list']
        subtotal = round(quantity * price, 2)

        item_dict = {
            'name': item['name'],
            'product': product,
            'quantity': quantity,
            'price': price,
            'prop_list': prop_list,
            'subtotal': subtotal,
        }
        cart_products.append(item_dict)

    if len(cart_products) > 0:
        context['cart_products'] = cart_products

    return context


def sort_queryset(queryset, sort):
    """
    Sorts a model queryset, with support for sets of multiple models
    """
    if 'favourites' in sort:
        return queryset
    else:
        if isinstance(queryset, list):
            reverse = '-' in sort
            sort = sort.replace('-', '')
            new_query = sorted(
                queryset,
                key=lambda obj: getattr(obj, sort),
                reverse=reverse
            )
            return new_query
        else:
            return queryset.order_by(sort)


def get_product_by_name(name):
    """
    Gets a product from either the BreadProduct or
    PastryProduct model with the specified name
    """
    bread = BreadProduct.objects.filter(name=name)
    if len(bread) > 0:
        return bread[0]
    else:
        return get_object_or_404(PastryProduct, name=name)
