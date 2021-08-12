from django.shortcuts import render

from orders.models import Order
from .models import Address
from django.core.exceptions import ObjectDoesNotExist


def updateAddress(request):
    shipping_addres = Address.objects.filter(user=request.user, address_type='S', default=True)
    order = Order.objects.get(user=request.user, ordered=False)
    try:

        if request.method == 'POST':
            firstname = request.POST['fname']
            lastname = request.POST['lname']
            phone1 = request.POST['phone1']
            phone2 = request.POST['phone2']
            delveryAddress = request.POST['delveryAddress']
            stateregion = request.POST['stateregion']
            city2 = request.POST['city2']
            # set_default_shipping_addres = request.POST['set_default_shipping_addres']

            if shipping_addres:
                shipping_addres.update(firstname=firstname)
                shipping_addres.update(lastname=lastname)
                shipping_addres.update(mobile_phone=phone1)
                shipping_addres.update(mobile=phone2)
                shipping_addres.update(delivery_address=delveryAddress)
                shipping_addres.update(region=stateregion)
                shipping_addres.update(city=city2)
    except  ObjectDoesNotExist:
        print('No such address found')

    return render(request, 'checkout.html', {'shipping_addres': shipping_addres, 'order':order})
