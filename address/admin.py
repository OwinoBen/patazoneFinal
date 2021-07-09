from django.contrib import admin
from .models import Address


# Register your models here.
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'delivery_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'delivery_address', 'zip']


admin.site.register(Address,AddressAdmin)
