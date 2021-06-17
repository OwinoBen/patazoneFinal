# Generated by Django 3.2.3 on 2021-06-17 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20210617_0126'),
        ('carts', '0011_auto_20210617_0233'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(blank=True, null=True, to='products.Product'),
        ),
    ]
