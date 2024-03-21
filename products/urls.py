from django.urls import path
from . import views


urlpatterns = [
     path('', views.ProductList.as_view(), name='product_list'),
     path('<str:product_name>', views.ProductDetail.as_view(),
          name='product_detail'),
     path('favorite/<str:product_name>',
          views.AddToFavorites.as_view(),
          name='add_to_favorites'),
     path('add/', views.AddProduct.as_view(), name='add_product'),
     path('edit/<str:product_name>', views.EditProduct.as_view(),
          name='edit_product'),
     path('validate_product/', views.validate_add_product,
          name='validate_product'),
]
