from django.shortcuts import render
from accounts.models import User


# Create your views here.

def adminpage(request):
    return render(request, 'dashboard/dashboard.html')


def userList(request):
    user = User.objects.all()
    context = {'user': user}
    return render(request, 'users/users.html', context)


def addUsers(request):
    return render(request,'users/addUser.html')