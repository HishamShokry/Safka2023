from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    mobile_number = models.CharField(max_length=11, null=True, blank=True, unique=True, db_index=True)
    facebook_page_url = models.URLField(max_length=200, blank=True)
    store_name = models.CharField(max_length=200, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', default='default_profile.jpg', blank=True, null=True)
    allow_upload_excel = models.BooleanField(default=False)

    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    PENDING = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    POSTPONED = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    PREPARATION = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    CANCELED_DURING_PREPARATION = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    SHIPPED = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    DELIVERED = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    RETURN_IN_PROGRESS = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    CANCELED = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    RETURNED = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    RETURNE_REQUESTS = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    RETURNED_AFTER_DELIVERY = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    is_admin = models.BooleanField('Is Admin', default=False)
    is_vendor = models.BooleanField('Is Vendor', default=False)
    is_marketer = models.BooleanField('Is Marketer', default=False)


    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super(User, self).save(*args, **kwargs)




        