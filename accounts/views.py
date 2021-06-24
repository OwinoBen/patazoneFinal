from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import *
from django.http import JsonResponse
from django.conf import settings
from orders.models import UserProfile
from accounts.models import User


def createAccount(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password_confirmation']:
            try:
                user = User.objects.get(username=request.POST['username'])
                email = User.objects.get(email=request.POST['email'])
                return render(request, 'accounts/register.html',
                              {'error': 'username and/or email has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(email=request.POST['email'], username=request.POST['username'],
                                                password=request.POST['password'],
                                                first_name=request.POST['firstname'],
                                                last_name=request.POST['lastname'])
                login(request, user)
                userProfile = UserProfile()
                print("creating new user profile")
                userProfile.user = request.user
                userProfile.save()
        else:
            return render(request, 'accounts/register.html', {'error': 'passwords should match'})
    else:
        return render(request, 'accounts/register.html')
    return render(request, 'accounts/register.html')


def whishlist(request):
    context = {}
    return render(request, 'whishlist/whishlist.html', context)


def Login(request):
    if request.method == "POST":
        user = authenticate(email=request.POST['email'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            if user.is_staff:
                # return redirect('admindashboard')
                return "this is staff user"
            else:
                return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Username or password is incorrect!'})
    else:
        return render(request, 'accounts/login.html')
    return render(request, 'accounts/login.html')


def Logout(request):
    logout(request)
    return redirect('home')
