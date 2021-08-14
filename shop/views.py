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
    pager = request.GET.get('value')
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


def SortedProductList(request, keyword):
    if keyword == 'shop':
        shopList = Product.objects.all().order_by('-id')
        search = request.GET.get('search')
        if search != '' and search is not None:
            shopList = shopList.filter(Q(title__icontains=search) | Q(price__icontains=search)).distinct()
        return render(request, 'shop.html', {'shopList': shopList})
    else:
        shopList = Product.objects.filter(category__iexact=str(keyword)).order_by('-id')
        search = request.GET.get('search')
        if search != '' and search is not None:
            shopList = shopList.filter(Q(title__icontains=search) | Q(price__icontains=search)).distinct()
        return render(request, 'shop.html', {'shopList': shopList})


def SortedProductSubcategory(request, keyword):
    if keyword == 'shop':
        shopList = Product.objects.all()
        search = request.GET.get('search')
        if search != '' and search is not None:
            shopList = shopList.filter(Q(title__icontains=search) | Q(price__icontains=search)).distinct()
        return render(request, 'shop.html', {'shopList': shopList})
    else:
        shopList = Product.objects.filter(subcategory__iexact=str(keyword))
        search = request.GET.get('search')
        if search != '' and search is not None:
            shopList = shopList.filter(Q(title__icontains=search) | Q(price__icontains=search)).distinct()
        return render(request, 'shop.html', {'shopList': shopList})


def SortedProductminorCategory(request, keyword):
    if keyword == 'shop':
        shopList = Product.objects.all().order_by('-id')
        search = request.GET.get('search')
        if search != '' and search is not None:
            shopList = shopList.filter(Q(title__icontains=search) | Q(price__icontains=search)).distinct()
        return render(request, 'shop.html', {'shopList': shopList})
    else:
        shopList = Product.objects.filter(minorCategory__iexact=str(keyword))
        search = request.GET.get('search')
        if search != '' and search is not None:
            shopList = shopList.filter(Q(title__icontains=search) | Q(price__icontains=search)).distinct()
        return render(request, 'shop.html', {'shopList': shopList})
