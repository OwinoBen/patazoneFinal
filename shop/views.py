from django.shortcuts import render
from products.models import *


# Create your views here.
def shopViews(request):
    shopList = Product.objects.all()
    context = {'shopList': shopList}
    return render(request, 'shop.html', context)
