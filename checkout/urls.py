from django.urls import path
from . import views
from .webhooks import webhook


urlpatterns = [
     path('', views.Checkout.as_view(), name='checkout'),
     path('success/<str:order_no>', views.CheckoutSuccess.as_view(),
          name='checkout_success'),
     path('wh/', webhook, name='webhook')
]