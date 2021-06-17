from django.contrib import admin
from .models import Order, ProductPurchase,OrderItem

admin.site.register(Order)

admin.site.register(ProductPurchase)
admin.site.register(OrderItem)
