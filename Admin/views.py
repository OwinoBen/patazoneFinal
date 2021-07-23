from django.contrib import messages
from django.contrib.auth import *
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from accounts.models import User, vendorBusinessInfo, shopInfo, VendorPaymentInfo
from address.models import Address
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

                    userprofile = UserProfile()
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
    vendorPrifix = "#VNDR"
    vendorID = (vendorPrifix + create_ref_code())

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
                    vendor = vendorBusinessInfo()
                    vendor.sellerid = vendorID
                    vendor.user = request.user
                    vendor.save()
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


def vendorAccountInformation(request):
    phoneNumber = request.POST['phone']
    phoneNumber2 = request.POST['phone2']
    gender = request.POST['gender']
    address = request.POST['address']
    city = request.POST['city']
    country = request.POST['country']
    nationalID = request.POST['nationalID']
    idphoto = request.FILES['idPhoto']
    organization = request.POST['organization']
    bstype = request.POST['bstype']
    totalEmployees = request.POST['totalEmployess']
    regNo = request.POST['regNo']
    regDoc = request.FILES['regDoc']
    kra = request.POST['kra']
    kraCopy = request.FILES['kraCopy']
    vat = request.POST['vat']
    shopname = request.POST['shopname']
    licenses = request.POST['license']
    pcategory = request.POST['pcategory']
    productrange = request.POST['productrange']
    payment_mode = request.POST['payment_mode']
    mpesaname = request.POST['mpesaname']
    mpesaNumber = request.POST['mpesaNumber']
    bankname = request.POST['bankname']
    accountname = request.POST['accountname']
    accountnumber = request.POST['accountnumber']
    bankcode = request.POST['bankcode']
    bankbranch = request.POST['bankbranch']
    email = request.POST['email']

    if request.method == "POST":
        if phoneNumber != '' and gender != '' and address != '' and city != '' and country != '' and nationalID != '' and idphoto != '' and regNo != '' and regDoc != '' and kra != '' and kraCopy != '' and shopname != '' and vat != '':

            try:
                shopname = shopInfo.objects.get(shopName= shopname)
                if shopname.exists():
                    messages.error(request, "Shop name already exists")
                    return render(request, 'auth/profile.html')
            except:
                vendor = User.objects.get(email=email)
                shop = shopInfo()
                vendorInfo = vendorBusinessInfo()
                vendorpayment = VendorPaymentInfo()
                adress = Address()

                adress.user = request.user
                adress.firstname = vendor.first_name
                adress.lastname = vendor.last_name
                adress.mobile = phoneNumber
                adress.mobile_phone = phoneNumber2
                adress.city = city
                adress.country = country
                adress.save()

                shop.user = request.user
                shop.shopName = shopname
                shop.shopLicense = licenses
                shop.productCategory = pcategory
                shop.productsell_range = productrange
                shop.save()

                vendorInfo.shop = shop
                vendorInfo.user=request.user
                vendorInfo.business_Registration_No = regNo
                vendorInfo.businessDocImage = regDoc
                vendorInfo.business_type = bstype
                vendorInfo.employessRange = totalEmployees
                vendorInfo.nationalID_Passport_No = nationalID
                vendorInfo.id_photo = idphoto
                vendorInfo.kraPin = kra
                vendorInfo.KRAimage = kraCopy
                vendorInfo.VAT_Registered = vat
                vendorInfo.phone_number = phoneNumber
                vendorInfo.phone_number2 = phoneNumber2
                vendorInfo.Address = adress
                vendorInfo.save()

                vendorpayment.user = request.user
                vendorpayment.mode_of_payment = payment_mode
                vendorpayment.mpesa_name = mpesaname
                vendorpayment.mpesa_Number = mpesaNumber
                vendorpayment.bank_name = bankname
                vendorpayment.bank_account_number = accountnumber
                vendorpayment.account_name = accountname
                vendorpayment.bank_code = bankcode
                vendorpayment.branch = bankbranch
                vendorpayment.save()

                return redirect('Admins:admin-home')
        else:
            messages.error(request, 'Please fill all the required fields.')
            return render(request, 'auth/profile.html')
    return render(request, 'auth/profile.html')
