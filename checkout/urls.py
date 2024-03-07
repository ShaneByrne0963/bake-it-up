from django.urls import path
from . import views


urlpatterns = [
     path('', views.Checkout.as_view(), name='checkout'),
     path('success', views.CheckoutSuccess.as_view(),
          name='checkout_success'),
]