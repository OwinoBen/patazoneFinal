from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.

def createAccount(request):
    context = {}
    return render(request, "register.html")


def login(request):
    context = {}
    return render(request, "login.html")


def whishlist(request):
    context = {}
    return render(request, 'whishlist/whishlist.html', context)
