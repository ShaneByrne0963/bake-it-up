from django.shortcuts import get_object_or_404
from django.db.models import Q, Count

from products.models import BreadProduct, PastryProduct
from .shortcuts import price_as_float, find_dict_in_list
from .constants import PRODUCT_PROPERTIES

from itertools import chain
import json
import os


# region List of Available Context Keys for global_context
"""
{
    modal_show {String}: Shows the modal on page load if
        exists. The string value indicates the form to be
        displayed in the modal, if any
    
    modal_load_fade {Truthy Expression}: Allows the modal fade
        animation on page load

    modal_form_errors {JSON}: A list of errors to be
        displayed in a modal form
    
    modal_form_type {String}: Describes the on-load form's specific
        purpose if a form is used in multiple instances
    
    login_custom_redirect {String}: A redirect string which will
        take the user to a custom url on login (Is cleared
        when the modal is closed)

    val_login {String}: The prefilled value for the login username

    val_remember {Truthy Expression}: Checks the login "Remember Me"
        checkbox
    
    val_username {String}: The prefilled value for the signup username

    val_email {String}: The prefilled value for the signup email address

    val_note {String}: The prefilled value for the user's note in
        the cart
    
    invalid_contact_details {Truthy Expression}: Shows the profile contact
        details form instead of the list on page load
    
    invalid_billing_details {Truthy Expression}: Shows the profile billing
        details form instead of the list on page load
    
    The following are prefilled values for the profile {String}
    val_profile_fname
    val_profile_lname
    val_profile_email
    val_profile_phone
    val_profile_line1
    val_profile_line2
    val_profile_city
    val_profile_county
    val_profile_country 
    
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


def get_add_product_context(request):
    """
    Returns the base context, with 2 objects used to
    build the properties forms for the Add/Edit Product
    pages
    """
    context = get_base_context(request)
    bread_properties = [
        {'label': 'Shapes', 'value': 'shape'},
        {'label': 'Sizes', 'value': 'size'},
        {'label': 'Contents', 'value': 'contents'},
    ]
    pastry_properties = [
        {'label': 'Types', 'value': 'type'},
        {'label': 'Contents', 'value': 'contents'},
        {'label': 'Colours', 'value': 'color'},
        {'label': 'Icing', 'value': 'icing'},
        {'label': 'Decoration', 'value': 'decoration'},
    ]
    # Getting the default labels and answers for each property
    for bread in bread_properties:
        default_label = find_dict_in_list(
            PRODUCT_PROPERTIES,
            'name',
            bread['value']
        )['default_label']
        bread['default_label'] = default_label

    for pastry in pastry_properties:
        default_label = find_dict_in_list(
            PRODUCT_PROPERTIES,
            'name',
            pastry['value']
        )['default_label']
        pastry['default_label'] = default_label

    context['bread_properties'] = bread_properties
    context['pastry_properties'] = pastry_properties
    return context


def get_products(request, **kwargs):
    """
    Gets a list of all products, with the option to
    filter by category, and sort
    """
    category = kwargs['category'] if 'category' in kwargs else 'all'
    sort = kwargs['sort'] if 'sort' in kwargs else 'favourites'
    q = kwargs['q'] if 'q' in kwargs else None
    favorites = kwargs['favorites'] if 'favorites' in kwargs else False

    products = None
    breads = None
    pastries = None

    if favorites:
        profile = request.user.profile
        breads = profile.favorite_breads.all()
        pastries = profile.favorite_pastries.all()
    else:
        breads = BreadProduct.objects.all()
        pastries = PastryProduct.objects.all()
    if q:
        breads = breads.filter(
            Q(display_name__icontains=q) | \
            Q(description__icontains=q)
        )
        pastries = pastries.filter(
            Q(display_name__icontains=q) | \
            Q(description__icontains=q)
        )

    # Product filtering
    if category == 'all':
        products = list(chain(breads, pastries))
    elif category == 'bread':
        products = breads
    elif category == 'pastries':
        products = pastries
    else:
        products = pastries.filter(category__name='cakes')

    if sort:
        sort = sort.replace('name', 'display_name')
        return sort_queryset(products, sort)
    return products


def sort_queryset(queryset, sort):
    """
    Sorts a model queryset, with support for sets of multiple models
    """
    if 'favourites' in sort:
        if isinstance(queryset, list):
            reverse = '-' in sort
            sort = 'favorites'
            new_query = sorted(
                queryset,
                key=lambda obj: getattr(obj, sort).count(),
                reverse=reverse
            )
            return new_query
        else:
            reverse = '-' if '-' in sort else ''
            return queryset.annotate(num_favorites=Count('favorites')) \
                    .order_by(f'{reverse}num_favorites')
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


def add_field_error(field, message, parse=True):
    """
    Creates a form error attached to a field
    """
    form_error = {
        field: [{
            'message': message,
            'code': ''
        }]
    }
    if parse:
        return json.dumps(form_error)
    return form_error


def delete_product(product):
    """
    Removes a product, and its image, from the database
    """
    os.remove(product.image.path)
    product.delete()
