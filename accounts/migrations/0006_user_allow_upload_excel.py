# Generated by Django 4.2.6 on 2023-11-10 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_mobile_number_alter_user_profile_photo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='allow_upload_excel',
            field=models.BooleanField(default=False),
        ),
    ]
