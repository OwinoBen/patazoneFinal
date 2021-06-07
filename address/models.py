from django.db import models
from billing.models import BillingProfile

# Create your models here.
Address_type = (
    ('billing', 'Billing address'),
    ('shipping', 'Shipping address'),
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    name = models.CharField()
