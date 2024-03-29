from django.urls import path
from . import views


urlpatterns = [
     path('', views.ViewCart.as_view(), name='cart'),
     path('add/<str:product_name>', views.AddToCart.as_view(),
          name='add_to_cart'),
     path('edit/<int:item_index>', views.EditCartItem.as_view(),
          name='edit_cart_item'),
     path('remove/<int:item_id>', views.RemoveCartItem.as_view(),
          name='remove_cart_item'),
]