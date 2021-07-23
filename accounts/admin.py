from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import User

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import EmailActivation, GuestEmail, shopInfo, vendorBusinessInfo, VendorPaymentInfo

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('email', 'is_superuser', 'is_vendor', 'staff')
    list_filter = ('is_superuser', 'staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'email', 'password', 'image')}),
        ('Permissions', {'fields': ('is_superuser', 'staff', 'is_active', 'is_vendor')}),
    )
    add_fieldsets = (
        (
            None, {
                'classes': ('wide'),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ['email']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


class EmailActivationAdmin(admin.ModelAdmin):
    search_fields = ['email']

    class Meta:
        model = EmailActivation


admin.site.register(EmailActivation, EmailActivationAdmin)


class GuestEmailAdmin(admin.ModelAdmin):
    search_fields = ['email']

    class Meta:
        model = GuestEmail


admin.site.register(GuestEmail, GuestEmailAdmin)
admin.site.register(vendorBusinessInfo)
admin.site.register(shopInfo)
admin.site.register(VendorPaymentInfo)
