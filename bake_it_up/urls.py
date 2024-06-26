"""
URL configuration for bake_it_up project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from home.views import CustomLogin, CustomSignup

urlpatterns = [
    path('admin/', admin.site.urls),

    # Override Allauth's login/signup urls
    path('accounts/login', CustomLogin.as_view(), name='account_login'),
    path('accounts/signup', CustomSignup.as_view(), name='account_signup'),

    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
    path('userprofile/', include('profiles.urls')),
    path('contact/', include('contact.urls')),
    path('orders/', include('orders.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
