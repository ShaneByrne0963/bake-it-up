from django.urls import path
from . import views
from .webhooks import webhook


urlpatterns = [
     path('', views.Checkout.as_view(), name='checkout'),
     path('success/<str:order_no>', views.CheckoutSuccess.as_view(),
          name='checkout_success'),
     path('cache_data/', views.cache_checkout_data,
          name='cache_checkout_data'),
     path('get_discount/', views.get_discount_code, name='get_discount'),
     path('wh/', webhook, name='webhook')
]