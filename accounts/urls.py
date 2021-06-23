from django.urls import path
from .views import createAccount, whishlist

app_name = 'accounts'

urlpatterns = [
    
    path('register/', createAccount, name='account'),
    # path('mywishlist/', createAccount, name='account'),


]