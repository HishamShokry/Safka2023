# Generated by Django 4.2.7 on 2023-12-04 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliate', '0042_rename_total_items_price_orderitem_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='total',
        ),
        migrations.AddField(
            model_name='order',
            name='shiping_price',
            field=models.IntegerField(default=0),
        ),
    ]
