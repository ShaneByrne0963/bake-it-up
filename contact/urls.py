from django.urls import path
from . import views


urlpatterns = [
    path('', views.StoreContact.as_view(), name='store_contact'),
    path('messages/', views.ViewMessages.as_view(), name='view_messages'),
]
