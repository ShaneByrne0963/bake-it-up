from django.urls import path
from . import views


urlpatterns = [
    path('', views.ViewOrders.as_view(), name='view_orders'),
]
