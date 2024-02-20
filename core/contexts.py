from allauth.account.forms import LoginForm, SignupForm


def get_base_context(request):
    login_form = LoginForm()
    signup_form = SignupForm()
    context = {
        'login_form': login_form,
        'signup_form': signup_form,
    }
    return context
