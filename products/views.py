from django.shortcuts import render
from .models import *


# Create your views here.

def product(request):
    products = Product.objects.all().flashDeals()
    featured = Product.objects.all().featured()
    context = {
                'products': products,
                'featured': featured
               }
    return render(request, 'homepage.html', context)
