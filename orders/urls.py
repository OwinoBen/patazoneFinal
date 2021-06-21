from django.urls import path
from .views import checkoutView

app_name = "orders"
urlpatterns = [
    path(r'^checkout/$', checkoutView, name='checkout'),
]
