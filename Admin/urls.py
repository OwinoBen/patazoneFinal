from django.urls import path, include
from .views import *

app_name = "Admin"

urlpatterns = [
    path('', adminpage, name='admin-home'),
    path('users', userList, name='user'),
    ]
