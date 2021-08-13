from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
import random
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from patazoneEcommerce.aws.utils import ProtectedS3Storage
from patazoneEcommerce.storageLocation.utils import PublicMediaStorage
from patazoneEcommerce.utils import unique_slug_generator, get_filename

# Create your models here.
CATEGORY = (('Phones & Accessories', 'Phones & Accessories'),
            ('Electronics', 'Electronics'),
            ('Computer & Tablets', 'Computer & Tablets'),
            ('Home and Office', 'Home and Office'),
            ('Schooling', 'Schooling'),
            ('supermarket', 'Supermarket'),
            ('Beauty, Health & Hair', 'Beauty, Health & Hair'),
            ('Baby, kids & Maternity', 'Baby, kids & Maternity'),
            ('Cloths', 'Cloths'),
            ('Sports', 'Sports'),
            ('Household Appliances', 'Household Appliances'),
            ('Automotive', 'Automotive'),
            )
COLORS = (('Red', 'Red'),
          ('Blue', 'Blue'),
          ('Black', 'Black'),
          ('Yellow', 'Yellow'),
          ('Orange', 'Orange'),
          ('Green', 'Green'),
          ('Purple', 'Purple'),
          ('Maroon', 'Maroon'),
          ('Pink', 'Pink'),
          ('Violet', 'Violet'),
          ('White', 'White'),
          ('Indigo', 'Indigo'),
          )
SUBCATEGORIES = (('television', 'Television'),
                 ('home audio', 'Home audio'),
                 ('home appliances', 'Home Appliances'),
                 ('makeup', 'Makeup'),
                 ('oral care', 'Oral Care'),
                 ('hair care', 'Hair Care'),
                 ('health care', 'Health Care'),
                 ('luxury beauty', 'Luxury Beauty'),
                 ('personal care', 'Personal Care'),
                 ('mobile phones', 'Mobile Phones'),
                 ('tabulates', 'Tabulates'),
                 )

Minorcategory = (('smart tv', 'Smart Tv'),
                 ('led tv', 'Led Tv'),
                 ('projector', 'Projector'),
                 ('home theatre', 'Home Theatre'),
                 ('sound bars', 'Sound bars'),
                 ('speakers', 'Speakers'),
                 ('bateries', 'Bateries'),
                 ('cables', 'Cables'),
                 ('power protection', 'Power protection'),
                 ('charger', 'Charger'),
                 ('television accessories', 'Television Accessories'),
                 )


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return f"products/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def flashDeals(self):
        return self.filter(flash=True, active=True)

    def topselling(self):
        return self.filter(topsell=True, active=True)

    def newDeals(self):
        return self.filter(new=True, active=True)

    def onsaleDeals(self):
        return self.filter(onSale=True, active=True)

    def searchProduct(self, query):
        lookups = (Q(title__icontains=query) |
                   Q(description__icontains=query) |
                   Q(price__icontains=query) |
                   Q(tag__title__icontains=query)
                   )
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def filterAll(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def topselling(self):
        return self.get_queryset().topselling()

    def flashDeals(self):
        return self.get_queryset().flashDeals()

    def newDeals(self):
        return self.get_queryset().newDeals()

    def onSaleDeals(self):
        return self.get_queryset().onsaleDeals()

    def getProduct_by_id(self, id):
        queryset = self.get_queryset().filter(id=id)
        if queryset.count() == 1:
            return queryset.first()
        return None

    def search(self, query):
        return self.get_queryset().active().searchProduct(query)


class Product(models.Model):
    title = models.CharField(max_length=120)
    sku = models.CharField(max_length=120, null=True)
    category = models.CharField(max_length=120, choices=CATEGORY, default="Phones and Electronics")
    subcategory = models.CharField(max_length=120, choices=SUBCATEGORIES, null=True, blank=True)
    minorCategory = models.CharField(max_length=120, choices=Minorcategory, null=True, blank=True)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    description = models.TextField()
    shortdescription = models.TextField(blank=True, null=True)
    tag = models.TextField(blank=True, null=True)
    brand = models.CharField(max_length=120, blank=True, null=True)
    cost_price = models.FloatField(default=0.00)
    price = models.FloatField(default=0.00)
    old_price = models.FloatField(default=0.00)
    quantity = models.IntegerField(default=1)
    discount_price = models.FloatField(default=0.00)
    image = models.FileField(upload_to=upload_image_path, storage=PublicMediaStorage(), null=True, blank=True)
    color = models.CharField(max_length=120, choices=COLORS, default='Black')
    size = models.CharField(max_length=20, null=True, blank=True)
    variation = models.CharField(max_length=20, null=True, blank=True)
    weight = models.CharField(max_length=20, null=True, blank=True)
    battery = models.CharField(max_length=120, null=True, blank=True)
    connectivity = models.CharField(max_length=120, blank=True, null=True)
    featured = models.BooleanField(default=False)
    topsell = models.BooleanField(default=False)
    flash = models.BooleanField(default=False)
    onSale = models.BooleanField(default=False)
    onsaleValue = models.IntegerField(default=0)
    new = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    upload_Date = models.DateTimeField(auto_now_add=True)
    is_digital = models.BooleanField(default=False)

    objects = ProductManager()

    def get_absolute_url(self):
        # return reverse("products:detail", kwargs={"slug": self.slug})
        # return reverse("products:detail", args=[str(self.slug)])
        return reverse("products:detail", args=(str(self.slug),))

    def get_add_to_cart_url(self):
        return reverse("cart:update", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("cart:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @property
    def get_name(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def get_downloads(self):
        querySet = self.productfile_set.all()
        return querySet


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)


def upload_product_file_loc(instance, filename):
    slug = instance.product.slug
    # id_ = 0
    id_ = instance.id
    if id_ is None:
        Klass = instance.__class__
        qs = Klass.objects.all().order_by('-pk')
        if qs.exists():
            id_ = qs.first().id + 1
        else:
            id_ = 0
    if not slug:
        slug = unique_slug_generator(instance.product)
    location = "product/{slug}/{id}/".format(slug=slug, id=id_)
    return location + filename


class SlideShow(models.Model):
    slide_id = models.CharField(max_length=120, null=True, blank=True)
    name = models.CharField(max_length=120, null=True, blank=True)
    tag1 = models.CharField(max_length=12, blank=True, null=True)
    tag2 = models.CharField(max_length=12, blank=True, null=True)
    tag3 = models.CharField(max_length=12, blank=True, null=True)
    file = models.FileField(storage=PublicMediaStorage())

    def __str__(self):
        return str(self.file.name)

    @property
    def display_name(self):
        og_name = get_filename(self.file.name)
        if self.name:
            return self.name
        return og_name

    def get_default_url(self):
        return self.product.get_absolute_url()


class ProductFile(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, null=True, blank=True)
    file = models.FileField(
        upload_to=upload_product_file_loc,
        storage=PublicMediaStorage(),  # FileSystemStorage(location=settings.PROTECTED_ROOT)
    )
    free = models.BooleanField(default=False)  # purchase required
    user_required = models.BooleanField(default=False)  # user doesn't matter

    def __str__(self):
        return str(self.file.name)

    @property
    def display_name(self):
        og_name = get_filename(self.file.name)
        if self.name:
            return self.name
        return og_name

    def get_default_url(self):
        return self.product.get_absolute_url()

    # def generate_download_url(self):
    #     bucket = getattr(settings, 'AWS_STORAGE_BUCKET_NAME')
    #     region = getattr(settings, 'S3DIRECT_REGION')
    #     access_key = getattr(settings, 'AWS_ACCESS_KEY_ID')
    #     secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY')
    #     if not secret_key or not access_key or not bucket or not region:
    #         return "/product-not-found/"
    #     PROTECTED_DIR_NAME = getattr(settings, 'PROTECTED_DIR_NAME', 'protected')
    #     path = "{base}/{file_path}".format(base=PROTECTED_DIR_NAME, file_path=str(self.file))
    #     aws_dl_object =  AWSDownload(access_key, secret_key, bucket, region)
    #     file_url = aws_dl_object.generate_url(path, new_filename=self.display_name)
    #     return file_url

    def get_download_url(self):
        return reverse("products:download",
                       kwargs={"slug": self.product.slug, "pk": self.pk}
                       )
