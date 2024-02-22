# region List of Available Context Keys
"""
{
    'modal_show' {String}: Shows the modal on page load if
        exists. The string value indicates the form to be
        displayed in the modal
    
    'modal_load_fade' {Truthy Expression}: Allows the modal fade
        animation on page load

    'modal_form_errors' {JSON}: A list of errors to be
        displayed in a modal form

    val_login {String}: The prefilled value for the login username

    val_remember {Truthy Expression}: Checks the login "Remember Me"
        checkbox
    
    val_username {String}: The prefilled value for the signup username

    val_email {String}
}
"""
# endregion

def get_base_context(request):

    # Getting any persistent context from the previous page
    context = request.session.pop('global_context', {})
    return context