# Generated by Django 4.2.7 on 2024-02-15 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliate', '0012_alter_request_amount_alter_request_bank_field_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='bank_field',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='instapay_field',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='vodafone_field',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]