# Generated by Django 2.2.14 on 2021-07-23 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210723_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendorbusinessinfo',
            name='KRAimage',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='vendorbusinessinfo',
            name='businessDocImage',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='vendorbusinessinfo',
            name='id_photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]