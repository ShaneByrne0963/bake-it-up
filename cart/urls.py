from django.urls import path
from . import views


urlpatterns = [
    path('add/<str:product_name>', views.AddToCart.as_view(),
         name='add_to_cart'),
]