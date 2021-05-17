from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

def createAccount(request):
    context = {}
    return render(request,"accounts/register.html")