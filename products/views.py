from django.shortcuts import render, redirect
from .models import *


# Create your views here.

def product(request):
    shopList = Product.objects.all().order_by('-id')
    products = Product.objects.all().flashDeals().order_by('-id')
    featured = Product.objects.all().featured().order_by('-id')
    pro_featured_count = Product.objects.count()
    electronics = Product.objects.filter(category='Electronics').order_by('-id')
    topselling =Product.objects.all().topselling().order_by('-id')
    slideshow = SlideShow.objects.all()
    search = request.GET.get('search')

    if search != '' and search is not None:
        shopList = shopList.filter(Q(title__icontains=search) | Q(price__icontains=search)).distinct()

    context = {
        'products': products,
        'featured': featured,
        'pro_featured_count': pro_featured_count,
        'slideshow': slideshow,
        'shopList': shopList,
        'topselling': topselling,
        'electronics': electronics,
    }
    return render(request, 'homepage.html', context)
