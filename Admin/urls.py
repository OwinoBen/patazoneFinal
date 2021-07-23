from django.urls import path, include
from .views import *

app_name = "Admin"

urlpatterns = [
    path('', adminpage, name='admin-home'),
    path('users', userList, name='user'),
    path('addusers', addUsers, name='adduser'),
    path('accountcreation', createVendorAccount, name='account'),
    path('login', Login, name='adminlogin'),
    path('completeregistration', vendorAccountInformation, name='completeregistration'),
    ]
