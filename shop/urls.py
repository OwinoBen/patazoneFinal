from django.urls import path
from .views import *

app_name = "shop"
urlpatterns = [
    path(r'^beautyhealth&hair/$', beautySearch, name='beauty'),
    path(r'^cloths/$', clothesSearch, name='clothes'),
    path(r'^computer&tablets/$', computerSearch, name='computer'),
    path(r'^electronics/$', electronicsSearch, name='electronics'),
    path(r'^grocery/$', grocerySearch, name='grocery'),
    path(r'^homeandoffice/$', homeOfficeSearch, name='homeOffice'),
    path(r'^householdappliances/$', householdSearch, name='houseHold'),
    path('Phones&Accessories/', phonesSearch, name='phones'),
    path('sortedproducts/<keyword>', SortedProductList, name="sortedproducts"),
    path('products/<keyword>', SortedProductSubcategory, name="sortedproductsubcategory"),
    path('productsview/<keyword>', SortedProductminorCategory, name="sortedproductminorcategory"),
]
