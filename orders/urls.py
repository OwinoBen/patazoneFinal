from django.urls import path
from .views import *

app_name = "orders"
urlpatterns = [
    path(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    path(r'^address/$', saveAddress, name='address'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
]
