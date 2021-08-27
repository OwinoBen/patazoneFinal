import re
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render

from address.models import Address

from django.http import JsonResponse, request
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Mpesa_Payments

from django.conf import settings

from .online import lipa_na_mpesa_online
from orders.models import Order, Payment
from django.core.mail import send_mail

HOST_USER_EMAIL = settings.EMAIL_HOST_USER


def payment(request):
    context = {
        'payments': Mpesa_Payments.objects.all()
    }
    return render(request, 'mpesaApp/payment.html', context)


@csrf_exempt
@require_http_methods(["POST", "GET"])
def lipa_na_mpesa(request):
    try:
        payment = Mpesa_Payments()
        req = json.loads(request.body.decode("utf-8"))
        payment.MerchantRequestID = req['Body']['stkCallback']['MerchantRequestID']
        payment.CheckoutRequestID = req['Body']['stkCallback']['CheckoutRequestID']
        payment.Amount = req['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
        payment.MpesaReceiptNumber = req['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
        payment.TransactionDate = req['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value']
        payment.PhoneNumber = req['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value']
        payment.save()


    except:
        pass

    return JsonResponse({})


def completeOrder(request):
    payment = Mpesa_Payments()
    payment.user = request.user
    payment.status = 1
    payment.save()
    if payment:
        order = Order.objects.get(user=request.user, ordered=False)
        orderitems = order.cart.all()
        orderitems.update(ordered=True)
        for item in orderitems:
            item.save()
        order.ordered = True
        order.payment = payment
        order.save()
    else:
        print("order not saved try again later")


def fetch_payments(request):
    payment_list = list(
        Mpesa_Payments.objects.values('id', 'MerchantRequestID', 'CheckoutRequestID', 'Amount', 'MpesaReceiptNumber',
                                      'TransactionDate', 'PhoneNumber', 'Status'))
    return JsonResponse(payment_list, safe=False)


def is_phone_number_valid(phone):
    pattern = "^0(7(?:(?:[129][0-9])|(?:0[0-8])|(4[0-1]))[0-9]{6})$"
    # pattern = re.compile("^(?:254|\\+254|0)?(7(?:(?:[12][0-9])|(?:0[0-8])|(?:9[0-2]))[0-9]{6})$")
    matched = re.match(pattern, phone)
    print(matched)
    return matched


def MpesaPayments(request):
    shipping_address = Address.objects.filter(user=request.user, address_type='S', default=True)
    orderTotal = Order.objects.get(user=request.user, ordered=False)
    totalamount = orderTotal.get_total()
    if request.method == 'POST':
        form = MpesaForm(request.POST)
        PhoneNumber = request.POST['PhoneNumber']
        if is_phone_number_valid('0746180701'):
            print("phone valid")
        else:
            print("phone not valid")
        Amount = request.POST['Amount']
        request.session["amount"] = totalamount
        if PhoneNumber != "" and Amount != "":
            phone_code = '254'
            lipa_na_mpesa_online(Amount, PhoneNumber)
            request.session["phone_number"] = (phone_code + PhoneNumber)
            return redirect('mpesa:completeorder')

    return render(request, 'checkout.html', {'order': orderTotal, 'shipping_address': shipping_address})


def PaymentDone(request, *args, **kwargs):
    error = None
    if request.method == 'POST':
        PhoneNumber = request.POST['phone']
        try:
            phoneNumber = Mpesa_Payments.objects.get(PhoneNumber=PhoneNumber, Status=0)
            if phoneNumber:
                order = Order.objects.get(user=request.user, ordered=False)
                orderitems = order.cart.all()
                orderitems.update(ordered=True)
                for item in orderitems:
                    item.save()
                order.ordered = True
                order.payment_receipt = phoneNumber.MpesaReceiptNumber
                order.paid_amount = phoneNumber.Amount
                order.customerNumber = PhoneNumber
                order.status = 'Pending'
                order.delivery = 'Customer delivery'
                order.payment_method = 'Mpesa payment'
                order.save()
                status = Mpesa_Payments.objects.filter(PhoneNumber=PhoneNumber, Status=0).update(Status=1)
                subject = 'Patazone marketplace, order placement'
                message = 'You have successfully placed an order with patazone marketplace.\n your order will be ' \
                          'shipped within two days '
                receipient = str(request.user.email)

                send_mail(subject, message, HOST_USER_EMAIL, [receipient], fail_silently=False)

                return redirect('register:orders')
            else:
                # return redirect('register:orders')
                print("No query matching your search")
        except ObjectDoesNotExist:
            messages.info(request, "Payment not received, continue with mpesa app snd wait for a minute")
            error = 'Payment not received, Check your phone to complete payment'
    context = {
        'error': error
    }

    return render(request, 'payment_done.html', context)
