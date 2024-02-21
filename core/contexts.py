from allauth.account.forms import LoginForm, SignupForm


# region List of Available Context Keys
"""
{
    'modal_show' {String}: Shows the modal on page load if
        exists. The string value indicates the form to be
        displayed in the modal

    'modal_form_errors' {JSON}: A list of errors to be
        displayed in a modal form

    val_login {String}: The prefilled value for the login username

    val_remember {Truthy Expression}: The prefilled value for the
        login "Remember Me" checkbox
    
    val_username {String}: The prefilled value for the signup username

    val_email {String}
}
"""
# endregion

def get_base_context(request):
    signup_form = SignupForm()
    context = {
        'signup_form': signup_form,
    }

    # Getting any persistent context from the previous page
    new_context = request.session.pop('global_context', {})
    context.update(new_context)

    return context
