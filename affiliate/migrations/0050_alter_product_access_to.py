# Generated by Django 4.2.7 on 2023-12-11 23:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('affiliate', '0049_alter_orderitem_order_alter_orderitem_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='access_to',
            field=models.ManyToManyField(limit_choices_to={'is_marketer': True}, related_name='access_to_this_product', to=settings.AUTH_USER_MODEL),
        ),
    ]
