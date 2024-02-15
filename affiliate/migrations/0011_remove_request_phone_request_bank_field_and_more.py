# Generated by Django 4.2.7 on 2024-02-15 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliate', '0010_alter_product_access_to_alter_product_barcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='phone',
        ),
        migrations.AddField(
            model_name='request',
            name='bank_field',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='request',
            name='instapay_field',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='request',
            name='vodafone_field',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]