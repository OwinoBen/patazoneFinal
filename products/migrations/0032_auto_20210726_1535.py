# Generated by Django 2.2.14 on 2021-07-26 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0031_auto_20210726_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
