# Generated by Django 4.2.7 on 2023-12-03 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('affiliate', '0032_rename_shipping_governorate_order_governorate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='governorate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='affiliate.shippingprice'),
        ),
    ]
