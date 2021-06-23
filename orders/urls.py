from django.urls import path
from .views import checkoutView, CheckoutView, PaymentView

app_name = "orders"
urlpatterns = [
    path(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
]
