from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Mpesa_Payments
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from requests.api import request
from .forms import MpesaForm, QueryForm
from .online import lipa_na_mpesa_online
from django.db.models import Q
from orders.models import Order
from django.utils.functional import cached_property


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
@require_http_methods(["POST"])
def lipa_na_mpesa(request):
    try:
        req = json.loads(request.body.decode("utf-8"))
        payment = Mpesa_Payments()
        payment.MerchantRequestID = req['Body']['stkCallback']['MerchantRequestID']
        payment.CheckoutRequestID = req['Body']['stkCallback']['CheckoutRequestID']
        payment.Amount = req['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
        payment.MpesaReceiptNumber = req['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
        payment.TransactionDate = req['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value']
        payment.PhoneNumber = req['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value']
        payment.user = request.user
        payment.save()

        if payment:
            order = Order.objects.get(ordered=False)
            orderitems = order.cart.all()
            orderitems.update(ordered=True)
            for item in orderitems:
                item.save()
            order.ordered = True
            order.payment = payment
            order.save()
        else:
            print("order not saved try again later")


    except:
        pass
    return JsonResponse({})


def fetch_payments(request):
    payment_list = list(
        Mpesa_Payments.objects.values('id', 'MerchantRequestID', 'CheckoutRequestID', 'Amount', 'MpesaReceiptNumber',
                                      'TransactionDate', 'PhoneNumber', 'Status'))
    return JsonResponse(payment_list, safe=False)


def MpesaPayments(request):
    if request.method == 'POST':
        form = MpesaForm(request.POST)
        if form.is_valid():
            PhoneNumber = form.cleaned_data['PhoneNumber']
            # Amount = Order.get_total
            Amount = form.cleaned_data['Amount']
            lipa_na_mpesa_online(Amount, PhoneNumber)

    form = MpesaForm()
    return render(request, 'mpesa.html', {'form': form})


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
