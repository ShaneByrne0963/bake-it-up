from django.urls import path
from . import views


urlpatterns = [
    path('', views.AccountSettings.as_view(), name='account_settings'),
    path('delete_account/', views.DeleteAccount.as_view(),
         name='delete_account'),
]
