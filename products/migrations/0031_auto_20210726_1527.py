# Generated by Django 2.2.14 on 2021-07-26 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0030_auto_20210726_0709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
