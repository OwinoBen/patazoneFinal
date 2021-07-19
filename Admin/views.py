from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from accounts.models import User

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
        if request.POST['username'] != '' and request.POST['email'] != '' and request.POST['fname'] != '' and \
                request.POST['lname'] != '':
            if request.POST['password'] == request.POST['confirmpass']:
                try:
                    user = User.objects.get(username=request.POST['username'])
                    email = User.objects.get(email=request.POST['email'])
                    return render(request, 'users/addUser.html',
                                  {'error': "User with the given credentials already exists"})
                except User.DoesNotExist:
                    user = User.objects.create_user(email=request.POST['email'], username=request.POST['username'],
                                                    first_name=request.POST['fname'],
                                                    last_name=request.POST['lname'],
                                                    password=request.POST['password'])
                    userprofile = UserProfile()
                    userprofile.user = user
                    userprofile.save()
                    messages.success(request, 'User successfully added')
                    return redirect('Admins:user')
            else:
                messages.error(request, 'The two passwords do not match')
                return render(request, 'users/addUser.html', {'error': 'he two passwords do not match'})
        else:
            return render(request, 'users/addUser.html', {'error': 'Please fill all the required fields'})

    return render(request, 'users/addUser.html')
