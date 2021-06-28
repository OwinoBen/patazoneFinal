from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [

    path('register/', createAccount, name='account'),
    path('login/', Login, name='login'),
    path('', Logout, name='logout'),
    path('myaccount', Myaccount, name='myaccount'),
    path('editaccountprofile/(?P<user_id>)/$', edit_profile, name='editprofile'),
    path('accountinfo', accountInfo, name='accountinfo'),
    path('addressbook', addressBook, name='addressbook'),
    path('mywhishlist', mywhishList, name='mywhishlist'),
    path('orders', orders, name='orders'),
    path('newslettersubscription', newsletter, name='newsletter'),
    path('vieworderdetails/(?P<id>)/$', OrderdetailView.as_view(), name='orderdetails'),
    # path('mywishlist/', createAccount, name='account'),

]
