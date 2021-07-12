import re
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from address.models import Address
from .models import Post
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Mpesa_Payments
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
from .forms import MpesaForm, QueryForm, CompleteOrder
from .online import lipa_na_mpesa_online
from django.db.models import Q
from orders.models import Order, Payment
from django.core.mail import send_mail

HOST_USER_EMAIL = settings.EMAIL_HOST_USER


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'mpesaApp/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'mpesaApp/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'mpesaApp/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateview(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def payment(request):
    context = {
        'payments': Mpesa_Payments.objects.all()
    }
    return render(request, 'mpesaApp/payment.html', context)


class Mpesa_PaymentsListView(ListView):
    model = Mpesa_Payments
    template_name = 'mpesaApp/payment.html'
    context_object_name = 'payments'
    ordering = ['-created_at']


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
            if phoneNumber.exists():
                order = Order.objects.get(user=request.user, ordered=False)
                orderitems = order.cart.all()
                orderitems.update(ordered=True)
                for item in orderitems:
                    item.save()
                order.ordered = True
                order.payment_receipt = phoneNumber.MpesaReceiptNumber
                order.paid_amount = phoneNumber.Amount
                order.status = ''
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


class Online_QueryListView(ListView):
    model = Mpesa_Payments
    template_name = 'mpesaApp/online_query.html'
    context_object_name = 'query'

    def get_queryset(self):
        query = self.request.GET.get('Query')
        if query:
            return Mpesa_Payments.objects.filter(
                Q(PhoneNumber__exact=query) |
                Q(MpesaReceiptNumber__exact=query) |
                Q(Amount__exact=query), Status=0
            )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = QueryForm(initial={
            'Query': self.request.GET.get('Query', ''),
        })

        return context


@require_http_methods(['POST'])
def update_status(self, *args, **kwargs):
    update = Mpesa_Payments.objects.get(Status=0)
    if update:
        update.value = 1
        update.save()
    super(Mpesa_Payments, self).update_status(*args, **kwargs)


from django.shortcuts import render

# Create your views here.
