# Generated by Django 2.2.14 on 2021-07-14 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0026_auto_20210714_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Phones & Accessories', 'Phones & Accessories'), ('Electronics', 'Electronics'), ('Computer & Tablets', 'Computer & Tablets'), ('Home and Office', 'Home and Office'), ('Schooling', 'Schooling'), ('Grocery', 'Grocery'), ('Beauty, Health & Hair', 'Beauty, Health & Hair'), ('Baby, kids & Maternity', 'Baby, kids & Maternity'), ('Cloths', 'Cloths'), ('Sports', 'Sports'), ('Household Appliances', 'Household Appliances'), ('Automotive', 'Automotive')], default='Phones and Electronics', max_length=120),
        ),
    ]
