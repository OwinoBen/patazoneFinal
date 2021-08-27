from django.urls import path, include
from .views import *

app_name = "mpesa"

urlpatterns = [

    path('make_payment/', MpesaPayments, name='mpesaApp-about'),


    path('api/fetch_payments/', fetch_payments, name='fetch_payments'),
    path('lipa_na_mpesa', lipa_na_mpesa, name='lipa_na_mpesa'),
    path('ordercompleted', PaymentDone, name='completeorder'),
]
