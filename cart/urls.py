from django.urls import path
from . import views


urlpatterns = [
     path('', views.ViewCart.as_view(), name='cart'),
     path('add/<str:product_name>', views.AddToCart.as_view(),
          name='add_to_cart'),
     path('clear', views.ClearCart.as_view(),
          name='clear_cart'),
]