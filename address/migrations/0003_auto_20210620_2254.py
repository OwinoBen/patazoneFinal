# Generated by Django 2.2.14 on 2021-06-20 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_adress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='adress',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]