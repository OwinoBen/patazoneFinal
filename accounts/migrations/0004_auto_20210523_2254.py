# Generated by Django 3.2.3 on 2021-05-23 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_is_superuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='staff',
            field=models.BooleanField(default=False),
        ),
    ]
