from django.urls import path
from .views import checkoutView,CheckoutView

app_name = "orders"
urlpatterns = [
    path(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
]
