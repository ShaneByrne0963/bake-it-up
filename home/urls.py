from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('login', views.CustomLogin.as_view(), name='login'),
    path('signup', views.CustomSignup.as_view(), name='signup'),
    path('email_confirmed', views.EmailConfirmed.as_view(),
         name='email_confirmed'),
]
