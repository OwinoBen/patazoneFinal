# Generated by Django 3.2.3 on 2021-06-14 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0006_alter_cart_subtotal'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]