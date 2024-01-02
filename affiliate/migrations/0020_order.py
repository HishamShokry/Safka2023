# Generated by Django 4.2.7 on 2023-11-30 16:08

import affiliate.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('affiliate', '0019_product_barcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='pending', max_length=255)),
                ('barcode', models.CharField(default=affiliate.models.generate_unique_barcode, max_length=8, unique=True)),
                ('client_name', models.CharField(max_length=255)),
                ('client_phone1', models.CharField(max_length=255)),
                ('client_phone2', models.CharField(max_length=255)),
                ('client_address', models.TextField()),
                ('shipping', models.IntegerField(default=0)),
                ('commission', models.IntegerField()),
                ('total', models.IntegerField()),
                ('note', models.TextField()),
                ('whats1_clicked', models.IntegerField(default=0)),
                ('phone1_clicked', models.IntegerField(default=0)),
                ('sms1_clicked', models.IntegerField(default=0)),
                ('whats2_clicked', models.IntegerField(default=0)),
                ('phone2_clicked', models.IntegerField(default=0)),
                ('sms2_clicked', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='affiliate.city')),
                ('marketer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='marketer_orders', to=settings.AUTH_USER_MODEL)),
                ('products', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='affiliate.product')),
                ('shipping_company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='affiliate.shippingcompany')),
                ('shipping_governorate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='affiliate.shippingprice')),
            ],
            options={
                'indexes': [models.Index(fields=['client_name', 'client_phone1', 'client_phone2', 'barcode', 'shipping_company'], name='affiliate_o_client__d4c4e2_idx')],
            },
        ),
    ]
