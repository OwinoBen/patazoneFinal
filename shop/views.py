from django.db.models import Q
from django.shortcuts import render
from products.models import *
from carts.models import Cart


# Create your views here.
def shopViews(request):
    shopList = Product.objects.all()
    objects = Cart.objects.all()
    onsale = Product.objects.onSaleDeals()
    search = request.GET.get('search')

    if search != '' and search is not None:
        shopList = shopList.filter(Q(title__icontains=search) | Q(price__icontains=search)).distinct()

    context = {'shopList': shopList,
               'onsale': onsale,
               'objects': objects
               }
    return render(request, 'shop.html', context)
