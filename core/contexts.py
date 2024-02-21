from allauth.account.forms import LoginForm, SignupForm


def get_base_context(request):
    login_form = LoginForm()
    signup_form = SignupForm()
    context = {
        'login_form': login_form,
        'signup_form': signup_form,
    }

    # Getting any persistent context from the previous page
    new_context = request.session.pop('global_context', {})
    context.update(new_context)

    return context
