# Generated by Django 2.2.14 on 2021-07-21 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0007_auto_20210709_1248'),
        ('accounts', '0002_auto_20210623_0404'),
    ]

    operations = [
        migrations.CreateModel(
            name='shopInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shopName', models.CharField(blank=True, max_length=120, null=True)),
                ('shopLicense', models.BooleanField(default=False)),
                ('productCategory', models.CharField(blank=True, max_length=120, null=True)),
                ('productsell_range', models.CharField(blank=True, max_length=120, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VendorPaymentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode_of_payment', models.CharField(blank=True, max_length=120, null=True)),
                ('mpesa_Number', models.CharField(blank=True, max_length=120, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=120, null=True)),
                ('account_name', models.CharField(blank=True, max_length=120, null=True)),
                ('bank_code', models.CharField(blank=True, max_length=120, null=True)),
                ('branch', models.CharField(blank=True, max_length=120, null=True)),
                ('mpesa_name', models.CharField(blank=True, max_length=120, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='vendorBusinessInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sellerid', models.CharField(blank=True, max_length=120, null=True)),
                ('email', models.CharField(blank=True, max_length=120, null=True)),
                ('business_type', models.CharField(blank=True, choices=[('company', 'Company'), ('partnership', 'Partnership'), ('individual', 'Individual')], max_length=120, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=120, null=True)),
                ('phone_number2', models.CharField(blank=True, max_length=120, null=True)),
                ('incharge', models.CharField(blank=True, max_length=120, null=True)),
                ('Identity', models.CharField(blank=True, choices=[('D', 'ID'), ('P', 'Passport')], max_length=120, null=True)),
                ('nationalID_Passport_No', models.CharField(blank=True, max_length=50, null=True)),
                ('id_photo', models.FileField(blank=True, null=True, upload_to='')),
                ('employessRange', models.CharField(blank=True, choices=[('one', '1-3'), ('four', '4-10'), ('eleven', '11-99'), ('hundred', '100 and more')], max_length=30, null=True)),
                ('business_Registration_No', models.CharField(blank=True, max_length=50, null=True)),
                ('businessDocImage', models.FileField(blank=True, null=True, upload_to='')),
                ('kraPin', models.CharField(blank=True, max_length=120, null=True)),
                ('KRAimage', models.FileField(blank=True, null=True, upload_to='')),
                ('VAT_Registered', models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No')], max_length=10, null=True)),
                ('Address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.Address')),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.shopInfo')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
