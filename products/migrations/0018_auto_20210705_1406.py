# Generated by Django 2.2.14 on 2021-07-05 14:06

from django.db import migrations, models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_auto_20210705_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slideshow',
            name='file',
            field=models.FileField(storage=storages.backends.s3boto3.S3Boto3Storage(location='protected'), upload_to=''),
        ),
    ]