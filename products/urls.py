from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProductList.as_view(), name='product_list'),
    path('<str:product_name>', views.ProductDetail.as_view(),
         name='product_detail'),
    path('add/<str:product_name>', views.AddToCart.as_view(),
         name='add_to_cart'),
]
