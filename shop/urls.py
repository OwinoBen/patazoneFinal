from django.urls import path
from .views import *

app_name = "shop"
urlpatterns = [
    path('sortedproducts/<keyword>', SortedProductList, name="sortedproducts"),
    path('products/<keyword>', SortedProductSubcategory, name="sortedproductsubcategory"),
    path('productsview/<keyword>', SortedProductminorCategory, name="sortedproductminorcategory"),
]
