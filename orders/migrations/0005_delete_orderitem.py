# Generated by Django 3.2.3 on 2021-06-17 02:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_orderitem'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
