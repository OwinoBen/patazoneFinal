from django.shortcuts import render
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


@csrf_protect
def addUsers(request):
    if request.method == 'POST':
        if request.POST['username'] != '' and request.POST['email'] != '' and request.POST['fname'] != '' and \
                request.POST['lname'] != '':
            try:
                username = User.objects.get(username=request.POST['username'])
                email = User.objects.get(email=request.POST['email'])
                return render(request, 'users/addUser.html',
                              {'error': "User with the given credentials already exists"})
            except User.DoesNotExist:
                user = User.objects.create_user(email=request.POST['email'], username=request.POST['username'],
                                                first_name=request.POST['firstname'],
                                                last_name=request.POST['lastname'],
                                                password=request.POST['password'])
                userprofile = UserProfile()
                userprofile.user = user
                userprofile.save()
                return re

    return render(request, 'users/addUser.html')
