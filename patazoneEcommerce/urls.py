"""patazonemarketplace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django import urls
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

import carts
from .views import homepage, aboutpage, contactus, frequentquiz, featured
from accounts.views import createAccount
from products.views import product
from shop.views import shopViews
from carts.views import cartView, updateCart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', product, name="home"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('about/', aboutpage, name="about"),
    path('contactus/', contactus, name="contact"),
    path('fqa_page/', frequentquiz, name="fqa"),
    path('accounts', createAccount, name="account"),
    path('featured', featured, name="featured"),
    path('shop', shopViews, name="shop"),
    path('cart_view', cartView, name="cart"),
    path(r'^cart/details', include(("carts.urls", carts), namespace='cart')),
    path('', include('accounts.urls', namespace="register")),
    path('Checkout', include('orders.urls', namespace="checkout")),
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
