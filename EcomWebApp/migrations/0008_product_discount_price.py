# Generated by Django 4.0.6 on 2022-10-10 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcomWebApp', '0007_product_outfit'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_price',
            field=models.FloatField(null=True),
        ),
    ]