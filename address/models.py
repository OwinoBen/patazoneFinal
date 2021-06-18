from django.conf import settings
from django.db import models
from django.urls import reverse
# from django_countries.fields import CountryField

from billing.models import BillingProfile

Address_type = (
    ('billing', 'Billing address'),
    ('shipping', 'Shipping address'),
)


class Adress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    # country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=120, choices=Address_type)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, blank=True, null=True, help_text='Shipping to? Who is it for?')
    nick_name = models.CharField(max_length=120, blank=True, null=True, help_text='Reference Name')
    address_type = models.CharField(max_length=120, choices=Address_type)
    address_line1 = models.CharField(max_length=120)
    address_line2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120, default='Kenya')
    postal_code = models.CharField(max_length=120)

    def __str__(self):
        if self.nick_name:
            return str(self.nick_name)
        return str(self.address_line1)

    def get_absolute_url(self):
        return reverse("address-update", kwargs={"pk": self.pk})

    def get_short_address(self):
        for_name = self.name
        if self.nick_name:
            for_name = "{}|{},".format(self.nick_name, for_name)
        return "{for_name}{line1},{city}".format(
            for_name=for_name or "",
            line1=self.address_line1,
            city=self.city
        )

    def get_address(self):
        return "{for_name}\n{line1}\n{line2}\n{city},{postal}\n{country}".format(
            for_name=self.name or "",
            line1=self.address_line1,
            line2=self.address_line2,
            city=self.city,
            postal=self.postal_code,
            country=self.country
        )
