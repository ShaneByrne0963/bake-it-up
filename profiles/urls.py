from django.urls import path
from . import views


urlpatterns = [
    path('', views.AccountSettings.as_view(), name='account_settings'),
]
