from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from orders.models import UserProfile

User = settings.AUTH_USER_MODEL


def createAccount(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password_confirmation']:
            try:
                user = User.objects.get(username=request.POST['username'])
                email = User.objects.get(email=request.POST['email'])
                return render(request, 'profile/profile_create.html',
                              {'error': 'username and/or email has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password'],
                                                email=request.POST['email'], first_name=request.POST['firstname'],
                                                last_name=request.POST['lastname'])
                login(request, user)
                userProfile = UserProfile
                userProfile.user = request.user
                userProfile.save()
        else:
            return render(request, 'accounts/register.html', {'error': 'passwords should match'})
    else:
        return render(request, 'accounts/register.html')


def login(request):
    context = {}
    return render(request, "login.html")


def whishlist(request):
    context = {}
    return render(request, 'whishlist/whishlist.html', context)


def Login(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admindashboard')
            else:
                return redirect('home')
        else:
            return render(request, 'profile/profile_login.html', {'error': 'Username or password is incorrect!'})
    else:
        return render(request, 'profile/profile_login.html')
