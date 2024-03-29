# Generated by Django 4.2.6 on 2023-11-05 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_facebook_page_url_user_mobile_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(blank=True, default='default_profile.jpg', null=True, upload_to='profile_photos/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='store_name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
