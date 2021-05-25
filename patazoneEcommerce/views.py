
from django.shortcuts import render
from django.http import JsonResponse


def homepage(request):
    context = {}
    return render(request, "homepage.html", context)


def aboutpage(request):
    context = {}
    return render(request, "about.html", context)

def contactus(request):
    context = {}
    return render(request, "contactus.html", context)

def frequentquiz(request):
    context = {}
    return render(request, "fqa.html", context)

def featured(request):
    context = {}
    return render(request, "featured.html", context)

