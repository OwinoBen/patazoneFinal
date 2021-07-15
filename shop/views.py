from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from products.models import *
from carts.models import Cart


# Create your views here.
def shopViews(request):
    objects = Cart.objects.all()
    onsale = Product.objects.onSaleDeals()
    search = request.GET.get('search')
    page = request.GET.get('page', 1)

    if search != '' and search is not None:
        products = Product.objects.filter(Q(title__icontains=search) | Q(price__icontains=search)).distinct()
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 12)
    try:
        shopList = paginator.page(page)
    except PageNotAnInteger:
        shopList = paginator.page(1)
    except EmptyPage:
        shopList = paginator.page(paginator.num_pages)



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


def SortedProductList(request, keyword):
    if keyword == 'shop':
        shopList = Product.objects.all()
        search = request.GET.get('search')
        if search != '' and search is not None:
            shopList = shopList.filter(Q(title__icontains=search) | Q(price__icontains=search)).distinct()
        return render(request, 'shop.html', {'shopList': shopList})
    else:
        shopList = Product.objects.filter(category__iexact=str(keyword))
        search = request.GET.get('search')
        if search != '' and search is not None:
            shopList = shopList.filter(Q(title__icontains=search) | Q(price__icontains=search)).distinct()
        return render(request, 'shop.html', {'shopList': shopList})


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
