import requests
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import *
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views import View
from django.views.decorators.csrf import csrf_protect

from accounts.forms import AccountUpdateForm
from mpesa.views import HOST_USER_EMAIL
from orders.models import UserProfile, Order
from address.models import Address
from accounts.models import User


# User = settings.AUTH_USER_MODEL


@csrf_protect
def createAccount(request):
    if request.method == 'POST':
        if request.POST['email'] != '' and request.POST['password'] != '' and request.POST['username'] != '':
            if request.POST['password'] == request.POST['password_confirmation']:
                try:
                    user = User.objects.get(username=request.POST['username'])
                    email = User.objects.get(email=request.POST['email'])
                    return render(request, 'accounts/register.html',
                                  {'error': 'username and/or email has already been taken'})
                except User.DoesNotExist:
                    user = User.objects.create_user(email=request.POST['email'], username=request.POST['username'],
                                                    first_name=request.POST['firstname'],
                                                    last_name=request.POST['lastname'],
                                                    password=request.POST['password'])

                    login(request, user)
                    userProfile = UserProfile()
                    userProfile.user = request.user
                    userProfile.save()
                    # sending email for successfull account creation
                    subject = 'Patazone marketplace, Account creation'
                    message = 'Thank you creating account with us'
                    receipient = str(request.user.email)
                    send_mail(subject, message, HOST_USER_EMAIL, [receipient], fail_silently=False)
            else:
                return render(request, 'accounts/register.html', {'error': 'passwords should match'})
        else:
            return render(request, 'accounts/register.html', {'error': 'Please fill required Fields'})
    else:
        return render(request, 'accounts/register.html')
    return redirect('home')


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
                    return redirect('home')
            else:
                return render(request, 'accounts/login.html', {'error': 'Username or password is incorrect!'})
        else:
            return render(request, 'accounts/login.html', {'error': 'Please fill all the required fields'})
    else:
        return render(request, 'accounts/login.html')
    return render(request, 'accounts/login.html')


def Logout(request):
    logout(request)
    return redirect('home')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


@login_required
def Myaccount(request):
    order_view = Order.objects.filter(user=request.user)
    shipping_address = Address.objects.filter(user=request.user, address_type='S', default=True)
    billing_address = Address.objects.filter(
        user=request.user,
        address_type='B',
        default=True
    )
    context = {
        'billing_address': billing_address,
        'shipping_address': shipping_address,
        'order_view': order_view
    }
    return render(request, 'myaccount/account.html', context)


@login_required
def accountInfo(request):
    context = {}
    return render(request, 'myaccount/accountInfo.html', context)


@login_required
def addressBook(request):
    context = {}
    return render(request, 'myaccount/addressbook.html', context)


class OrderdetailView(View):
    def get(self, request, id, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, order_id=id)
            context = {
                'object': order,
            }
            print(order)
            return render(self.request, 'myaccount/orderDetails.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")


@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'myaccount/orders.html', context)


@login_required
def mywhishList(request):
    context = {}
    return render(request, 'myaccount/whishlist.html', context)


@login_required
def newsletter(request):
    context = {}
    return render(request, 'myaccount/newsletter.html', context)


def edit_profile(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("register:login")

    user_id = kwargs.get("user_id")
    account = User.objects.get(pk=user_id)
    if account.pk != request.user.pk:
        return HttpResponse("You are not allowed to edit this profile")
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            new_firstname = form.cleaned_data['first_name']
            return redirect("register:account", user_id=account.pk)
        else:
            form = AccountUpdateForm(request.POST, instance=request.user,
                                     initial={
                                         "id": account.pk,
                                         # "email": account.email,
                                         "first_name": account.first_name,
                                         "last_name": account.last_name,
                                         # "hide_email": account.hide_email,
                                     }
                                     )
            context['form'] = form
    else:
        form = AccountUpdateForm(
            initial={
                "id": account.pk,
                # "email": account.email,
                "first_name": account.first_name,
                "last_name": account.last_name,
                # "hide_email": account.hide_email,
            }
        )
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, "myaccount/accountInfo.html", context)
