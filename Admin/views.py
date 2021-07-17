from django.shortcuts import render


# Create your views here.

def adminpage(request):
    return render(request, 'dashboard/dashboard.html')


def userList(request):
    return render(request, 'users/users.html')
