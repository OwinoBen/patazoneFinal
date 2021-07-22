from django.contrib import messages
from django.contrib.auth import *
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from accounts.models import User, vendorBusinessInfo
from carts.views import create_ref_code

# Create your views here.
from orders.models import UserProfile


def adminpage(request):
    return render(request, 'dashboard/dashboard.html')


def userList(request):
    user = User.objects.all()
    context = {'user': user}
    return render(request, 'users/users.html', context)


def addUsers(request):
    if request.method == 'POST':
        if request.POST['username'] != '' and request.POST['email'] != '' and request.POST['fullname'] != '' and \
                request.POST['lname'] != '':
            if request.POST['password'] == request.POST['confirmpass']:
                try:
                    user = User.objects.get(username=request.POST['username'])
                    email = User.objects.get(email=request.POST['email'])
                    return render(request, 'users/addUser.html',
                                  {'error': "User with the given credentials already exists"})
                except User.DoesNotExist:
                    user = User.objects.create_user(email=request.POST['email'], username=request.POST['username'],
                                                    first_name=request.POST['fullname'],
                                                    last_name=request.POST['lname'],
                                                    password=request.POST['password'])

                    vendorPrifix = "#VNDR"
                    vendorID = (vendorPrifix + create_ref_code())
                    userprofile = UserProfile()
                    vendor = vendorBusinessInfo()
                    vendor.sellerid = vendorID
                    vendor.user = user
                    vendor.save()
                    userprofile.user = user
                    userprofile.save()
                    messages.success(request, 'User successfully added')
                    return redirect('Admins:user')
            else:
                messages.error(request, 'The two passwords do not match')
                return render(request, 'users/addUser.html', {'error': 'he two passwords do not match'})
        else:
            messages.error(request, 'Please fill all the required fields')
            return render(request, 'users/addUser.html', {'error': 'Please fill all the required fields'})

    return render(request, 'users/addUser.html')


def createVendorAccount(request):
    if request.method == 'POST':
        if request.POST['username'] != '' and request.POST['email'] != '' and request.POST['fullname'] != '' and \
                request.POST['lname'] != '':
            if request.POST['password'] == request.POST['confirmpass']:
                try:
                    user = User.objects.get(username=request.POST['username'])
                    email = User.objects.get(email=request.POST['email'])
                    return render(request, 'users/addUser.html',
                                  {'error': "User with the given credentials already exists"})
                except User.DoesNotExist:
                    username = request.POST['username']
                    email = request.POST['email']
                    user = User.objects.create_user(email=email, username=username,
                                                    first_name=request.POST['fullname'],
                                                    last_name=request.POST['lname'],
                                                    password=request.POST['password'],
                                                    is_vendor=True)
                    login(request, user)
                    userprofile = UserProfile()
                    userprofile.user = user
                    userprofile.save()
                    request.session['username'] = username
                    request.session['email'] = email
                    messages.success(request, 'Welcome successfully added')
                    return redirect('Admins:admin-home')
            else:
                messages.error(request, 'The two passwords do not match')
                return render(request, 'users/addUser.html', {'error': 'he two passwords do not match'})
        else:
            messages.error(request, 'Please fill all the required fields')
            return render(request, 'users/addUser.html', {'error': 'Please fill all the required fields'})
    return render(request, 'auth/register.html')


def Login(request):
    if request.method == "POST":
        if request.POST['email'] != '' and request.POST['password'] != '':
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                if user.is_staff:
                    # return redirect('admindashboard')
                    return "this is staff user"
                else:
                    messages.success(request, 'Login success')
                    return redirect('Admins:admin-home')
            else:
                messages.success(request, 'User successfully added')
                return render(request, 'auth/register.html', {'error': 'Username or password is incorrect!'})
        else:
            return render(request, 'auth/register.html', {'error': 'Please fill all the required fields'})
    else:
        return render(request, 'auth/profile.html')

    return render(request, 'auth/profile.html')
