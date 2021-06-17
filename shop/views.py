from django.shortcuts import render
from products.models import *
from carts.models import Cart


# Create your views here.
def shopViews(request):
    shopList = Product.objects.all()
    objects = Cart.objects.all()
    onsale = Product.objects.onSaleDeals()
    context = {'shopList': shopList,
               'onsale': onsale,
               'objects':objects
               }
    return render(request, 'shop.html', context)



