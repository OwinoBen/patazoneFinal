from django.shortcuts import render
from products.models import *


# Create your views here.
def shopViews(request):
    shopList = Product.objects.all()
    onsale = Product.objects.onSaleDeals()
    context = {'shopList': shopList,
               'onsale': onsale
               }
    return render(request, 'shop.html', context)
