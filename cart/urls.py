from django.urls import path
from . import views


urlpatterns = [
     path('', views.ViewCart.as_view(), name='cart'),
     path('add/<str:product_name>', views.AddToCart.as_view(),
          name='add_to_cart'),
     path('remove/<int:item_id>', views.RemoveCartItem.as_view(),
          name='remove_cart_item'),
     path('clear', views.ClearCart.as_view(),
          name='clear_cart'),
]