from django.shortcuts import render
from .models import *




# Create your views here.

def product(request):
    products = Product.objects.all().flashDeals()
    featured = Product.objects.all().featured()
    pro_featured_count = Product.objects.count()
    context = {
        'products': products,
        'featured': featured,
        'pro_featured_count': pro_featured_count
    }
    return render(request, 'homepage.html', context)



