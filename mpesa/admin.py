from django.contrib import admin
from .models import Mpesa_Payments
from .models import Post


class Mpesa(admin.ModelAdmin):
    list_display = [
        'MerchantRequestID',
        'CheckoutRequestID',
        'Amount',
        'MpesaReceiptNumber',
        'TransactionDate',
        'PhoneNumber',
        'Status',
    ]
    list_filter = ['MpesaReceiptNumber', 'PhoneNumber', 'Status']
    search_fields = ['MpesaReceiptNumber', 'PhoneNumber', 'Status', 'TransactionDate']


admin.site.register(Mpesa_Payments, Mpesa)
admin.site.register(Post)
