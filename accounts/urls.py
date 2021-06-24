from django.urls import path
from .views import createAccount, whishlist,Login, Logout

app_name = 'accounts'

urlpatterns = [
    
    path('register/', createAccount, name='account'),
    path('login/', Login, name='login'),
    path('', Logout, name='logout'),
    # path('mywishlist/', createAccount, name='account'),


]