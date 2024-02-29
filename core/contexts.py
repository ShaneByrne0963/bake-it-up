from products.models import BreadProduct, PastryProduct
from django.shortcuts import get_object_or_404


# region List of Available Context Keys
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
}
"""
# endregion

def get_base_context(request):
    """
    Returns the context required for the base template to function
    """
    # Getting any persistent context from the previous page
    context = request.session.pop('global_context', {})
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
