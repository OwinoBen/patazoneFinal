from django.conf import settings
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField

from billing.models import BillingProfile

Address_type = (
    ('B', 'Billing address'),
    ('S', 'Shipping address'),
)


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)
    firstname = models.CharField(max_length=120, blank=True, null=True)
    lastname = models.CharField(max_length=120, blank=True, null=True)
    mobile_phone = models.CharField(max_length=120, blank=True, null=True)
    mobile= models.CharField(max_length=120, blank=True, null=True)
    delivery_address = models.TextField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100, null=True, blank=True)
    address_type = models.CharField(max_length=120, choices=Address_type)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = 'Addresses'
