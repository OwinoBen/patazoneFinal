# Generated by Django 2.2.14 on 2021-07-14 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0027_auto_20210714_1047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='backImage',
        ),
        migrations.RemoveField(
            model_name='product',
            name='sideImage',
        ),
    ]
