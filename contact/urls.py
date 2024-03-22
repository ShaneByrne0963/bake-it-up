from django.urls import path
from . import views


urlpatterns = [
    path('', views.StoreContact.as_view(), name='store_contact'),
    path('messages/', views.ViewMessages.as_view(), name='view_messages'),
    path('open_message/<int:message_id>', views.open_message,
         name='open_message'),
    path('delete_message/<int:message_id>', views.DeleteMessage.as_view(),
         name='delete_message'),
]
