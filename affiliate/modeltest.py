from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.postgres.indexes import GinIndex

# User model
class User(models.Model):
    role = models.CharField(max_length=255)
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    allow_upload_excel = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Admin model
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rule = models.ForeignKey('Rule', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Marketer model
class Marketer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Moderator model
class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    main_account = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moderator_accounts')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Merchant model
class Merchant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Category model
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['name'])]


# Notification model
class Notification(models.Model):
    ORDER_NOTE = 'order_note'
    REQUEST = 'request'
    ORDER_STATUS = 'order_status'
    TICKET = 'ticket'

    NOTIFICATION_TYPES = [
        (ORDER_NOTE, 'Order Note'),
        (REQUEST, 'Request'),
        (ORDER_STATUS, 'Order Status'),
        (TICKET, 'Ticket'),
    ]

    ADMIN = 'admin'
    MARKETER = 'marketer'
    MODERATOR = 'moderator'
    MERCHANT = 'merchant'

    USER_ROLES = [
        (ADMIN, 'Admin'),
        (MARKETER, 'Marketer'),
        (MODERATOR, 'Moderator'),
        (MERCHANT, 'Merchant'),
    ]

    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default=ORDER_NOTE)
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    for_role = models.CharField(max_length=20, choices=USER_ROLES)
    who = models.ManyToManyField(User, related_name='notifications')
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['type', 'is_read'])]

# OrderHistory model
class OrderHistory(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    serial_number = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    property_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    total_price = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['vendor'])]

# Reply model
class Reply(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Action model
class Action(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Request model
class Request(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

    REQUEST_STATUSES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    role = models.CharField(max_length=255)
    target = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.IntegerField()
    phone = models.IntegerField()
    payment_method = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=REQUEST_STATUSES, default=PENDING)
    note = models.TextField()
    reason = models.TextField()
    actions = models.ManyToManyField(Action)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['payment_method'])]

# Rule model
class Rule(models.Model):
    name = models.CharField(max_length=255, unique=True)
    permissions = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['name'])]

# ShippingCompany model
class ShippingCompany(models.Model):
    name = models.CharField(max_length=255, unique=True)
    site = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [GinIndex(fields=['name'])]

# Support model
class Support(models.Model):
    phone = models.CharField(max_length=255)
    description = models.TextField()
    for_role = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['phone', 'description'])]

# Warehouse model
class Warehouse(models.Model):
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [GinIndex(fields=['name'])]

# PriceList model
class PriceList(models.Model):
    governorate = models.IntegerField(unique=True)
    price = models.IntegerField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Product model
class Product(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    merchant = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    sale_price = models.IntegerField()
    purchase_price = models.IntegerField()
    image = models.CharField(max_length=255)
    description = models.TextField()
    note = models.TextField()
    media_url = models.CharField(max_length=255)
    properties = models.JSONField(default=list)
    is_active = models.BooleanField(default=False)
    access_type = models.CharField(max_length=255, choices=[('public', 'Public'), ('private', 'Private')], default='public')
    access_to = models.ManyToManyField(User, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [GinIndex(fields=['name', 'barcode', 'access_type'])]

# Order model
class Order(models.Model):
    PENDING = 'pending'

    status = models.CharField(max_length=255, default=PENDING)
    holding_to = models.DateTimeField(null=True, blank=True)
    serial_number = models.CharField(max_length=255, unique=True)
    marketer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='marketer_orders')
    moderator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='moderator_orders')
    client_name = models.CharField(max_length=255)
    client_phone1 = models.CharField(max_length=255)
    client_phone2 = models.CharField(max_length=255)
    client_address = models.TextField()
    shipping_governorate = models.ForeignKey(PriceList, on_delete=models.CASCADE)
    city = models.IntegerField()
    shipping = models.IntegerField(default=0)
    shipping_company = models.ForeignKey(ShippingCompany, on_delete=models.SET_NULL, null=True, blank=True)
    commission = models.IntegerField()
    page_name = models.CharField(max_length=255, trim=True)
    items = models.JSONField(default=list)
    total = models.IntegerField()
    note = models.TextField()
    replies = models.ManyToManyField(Reply)
    actions = models.ManyToManyField(Action)
    key = models.IntegerField(default=0)
    whats1_clicked = models.IntegerField(default=0)
    phone1_clicked = models.IntegerField(default=0)
    sms1_clicked = models.IntegerField(default=0)
    whats2_clicked = models.IntegerField(default=0)
    phone2_clicked = models.IntegerField(default=0)
    sms2_clicked = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['client_name', 'client_phone1', 'client_phone2', 'serial_number', 'shipping_company'])]
