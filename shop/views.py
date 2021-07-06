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


def beautySearch(request):
    shopList = Product.objects.filter(category='B')
    context = {'shopList': shopList}
    return render(request, 'menu/beauty.html', context)


def clothesSearch(request):
    shopList = Product.objects.filter(category='CL')
    context = {'shopList': shopList}
    return render(request, 'menu/clothes.html', context)


def computerSearch(request):
    shopList = Product.objects.filter(category='C')
    context = {'shopList': shopList}
    return render(request, 'menu/computer.html', context)


def electronicsSearch(request):
    shopList = Product.objects.filter(category='E')
    context = {'shopList': shopList}
    return render(request, 'menu/electronics.html', context)


def grocerySearch(request):
    shopList = Product.objects.filter(category='G')
    context = {'shopList': shopList}
    return render(request, 'menu/grocery.html', context)


def homeOfficeSearch(request):
    shopList = Product.objects.filter(category='H')
    context = {'shopList': shopList}
    return render(request, 'menu/homeoffice.html', context)


def householdSearch(request):
    shopList = Product.objects.filter(category='HA')
    context = {'shopList': shopList}
    return render(request, 'menu/household.html', context)


def phonesSearch(request):
    shopList = Product.objects.filter(category='P')
    context = {'shopList': shopList}
    return render(request, 'menu/phones.html', context)
