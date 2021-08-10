from django.urls import path
from .views import *

app_name = "orders"
urlpatterns = [
    path(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    path(r'^address/$', saveAddress, name='address'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('pay/<payment_option>/', pay, name='pay'),
    path('payondelivery/<payment_option>/', payondelivery, name='payondelivery'),
    path('confirmpayment/', confirmPayment, name='confirmpayment'),
    path('pickformstore/', order_pick_from_store, name='pickup'),
]
