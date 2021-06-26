from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Posts Models
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


# M-pesa Payment models
class Mpesa_Payments(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    MerchantRequestID = models.CharField(max_length=100, null=True, blank=True)
    CheckoutRequestID = models.CharField(max_length=100, null=True, blank=True)
    Amount = models.CharField(max_length=100, null=True, blank=True)
    MpesaReceiptNumber = models.CharField(max_length=100, null=True, blank=True)
    TransactionDate = models.CharField(max_length=100, null=True, blank=True)
    PhoneNumber = models.CharField(max_length=100, null=True, blank=True)
    Status = models.IntegerField(default=0)

    def __str__(self):
        return str(self.PhoneNumber)