from django.contrib import admin
from .models import *

admin.site.register(Order)

admin.site.register(ProductPurchase)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
