from django.urls import path
from . import views


urlpatterns = [
     path('', views.StoreContact.as_view(), name='store_contact'),
     path('messages/', views.ViewMessages.as_view(), name='view_messages'),
     path('open_message/<int:message_id>', views.open_message,
          name='open_message'),
     path('delete_message/<int:message_id>', views.DeleteMessage.as_view(),
          name='delete_message'),
     path('newsletter_signup', views.NewsletterSignup.as_view(),
          name='newsletter_signup'),
     path('send_newsletter', views.SendNewsletter.as_view(),
          name='send_newsletter'),
     path('check_code_name', views.check_code_name, name='check_code_name'),
     path('newsletter_unsubscribe/<str:email>',
          views.NewsletterUnsubscribe.as_view(),
          name='newsletter_unsubscribe')
]
