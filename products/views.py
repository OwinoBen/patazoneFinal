from django.shortcuts import render, redirect
from .models import *


# Create your views here.

def product(request):
    shopList = Product.objects.all()
    products = Product.objects.all().flashDeals()
    featured = Product.objects.all().featured()
    pro_featured_count = Product.objects.count()
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
    }
    return render(request, 'homepage.html', context)
