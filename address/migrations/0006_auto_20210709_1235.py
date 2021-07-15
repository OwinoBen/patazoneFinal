# Generated by Django 2.2.14 on 2021-07-09 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0005_auto_20210622_0401'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='street_address',
            new_name='city',
        ),
        migrations.AddField(
            model_name='address',
            name='delivery_address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='firstname',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='lastname',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='mobile',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='mobile_phone',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='region',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]