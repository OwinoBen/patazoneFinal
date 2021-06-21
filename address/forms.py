from django import forms
from .models import Address


# class AddressForm(forms.ModelForm):
#     class Meta:
#         model = Address
#         fields = [
#             'nick_name',
#             'name',
#             # 'billing_profile',
#             'address_type',
#             'address_line1',
#             'address_line2',
#             'city',
#             'country',
#             'postal_code'
#         ]
#
#
# class AddressCheckoutForm(forms.ModelForm):
#     class Meta:
#         model = Address
#         fields = [
#             'nick_name',
#             'name',
#             # 'billing_profile',
#             # 'address_type',
#             'address_line1',
#             'address_line2',
#             'city',
#             'country',
#             'postal_code'
#         ]
