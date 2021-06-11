from django.urls import path
from .views import (
        cart_home,
        updateCart,
        checkoutHome,
        checkoutDoneView
        )
urlpatterns =[
    path('', cart_home, name='home'),
    path(r'^checkout/success/$', checkoutDoneView, name='success'),
    path(r'^checkout/$', checkoutHome, name='checkout'),
    path(r'^update/$', updateCart, name='update'),
]