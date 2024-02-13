# Generated by Django 4.2.7 on 2024-02-13 06:35

import affiliate.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('affiliate', '0008_alter_request_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='barcode',
            field=models.CharField(db_index=True, default=affiliate.models.generate_unique_barcode, max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('طلبات معلقة', 'طلبات معلقة'), ('طلبات ملغيه', 'طلبات ملغيه'), ('طلبات مؤجلة', 'طلبات مؤجلة'), ('طلبات جاري التحضير', 'طلبات جاري التحضير'), ('طلبات ملغية اثناء التحضير', 'طلبات ملغية اثناء التحضير'), ('طلبات تم الشحن', 'طلبات تم الشحن'), ('طلبات تم التوصيل', 'طلبات تم التوصيل'), ('طلبات استرجاع من العميل', 'طلبات استرجاع من العميل'), ('طلبات مرتجعة بعد التوصيل', 'طلبات مرتجعة بعد التوصيل'), ('جار الاسترجاع', 'جار الاسترجاع'), ('مرتجع', 'مرتجع')], db_index=True, default='طلبات معلقة', max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='access_to',
            field=models.ManyToManyField(blank=True, limit_choices_to={'is_marketer': True}, null=True, related_name='access_to_this_product', to=settings.AUTH_USER_MODEL),
        ),
    ]
