# Generated by Django 4.2.7 on 2023-11-12 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('affiliate', '0008_alter_product_vendor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='category',
            name='updated_at',
        ),
    ]
