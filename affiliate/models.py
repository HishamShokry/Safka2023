from django.db import models
from accounts.models import User
from colorfield.fields import ColorField
from django.utils.safestring import mark_safe
import uuid
from smart_selects.db_fields import ChainedForeignKey
# Create your models here.


def generate_unique_barcode():
    # Generate a unique 8-digit barcode using UUID
    return 'SK'+str(uuid.uuid4().int)[:7]


def generate_unique_barcode_returned():
    # Generate a unique 8-digit barcode using UUID
    return 'SK'+str(uuid.uuid4().int)[:7]+'R'



# Warehouse model
class Inventory(models.Model):
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['name'])]
        verbose_name_plural = "inventories"  # Set the desired display name for the model in plural form

    def __str__(self):
        return self.name
    


# Category model
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    # inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['name'])]
        verbose_name_plural = "categories"  # Set the desired display name for the model in plural form

    def __str__(self):
        return self.name
    


# ShippingCompany model
class ShippingCompany(models.Model):
    name = models.CharField(max_length=255, unique=True)
    website = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['name'])]

    def __str__(self):
        return self.name


class Governorate(models.Model):
    governorate_name_ar = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.governorate_name_ar}"


class City(models.Model):
    governorate = models.ForeignKey(Governorate, on_delete=models.CASCADE)
    city_name_ar = models.CharField(max_length=200)
    city_name_en = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city_name_ar} ({self.city_name_en})"


class ShippingPrice(models.Model):
    governorate = models.ForeignKey(Governorate, on_delete=models.CASCADE)
    price = models.IntegerField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.governorate}"



class Size(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)
    color = ColorField(format="hexa")   

    def __str__(self):
        return self.name



class Product(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True, blank=True)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendor_products', null=True, blank=True, limit_choices_to={'is_vendor': True})
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    access_to = models.ManyToManyField(User, related_name='access_to_this_product', limit_choices_to={'is_marketer': True})
    name = models.CharField(max_length=255)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    # min_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    media_url = models.URLField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    access_type = models.CharField(max_length=255, choices=[('public', 'Public'), ('private', 'Private')], default='public')
    # Generate a random code using uuid for the combination of size and color
    barcode = models.CharField(max_length=10, unique=True, default=generate_unique_barcode)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


    class Meta:
        indexes = [models.Index(fields=['name', 'access_type'])]
        

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variant_set')
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.color} x {self.size}"



# Order model
class Order(models.Model):
    PENDING = 'pending'
    PREPARATION = 'preparation'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    RETURN_IN_PROGRESS = 'return_in_progress'
    CANCELED = 'canceled'
    POST_DELIVERY_RETURN = 'post_delivery_return'
    RETURNED = 'returned'
    RETURNED_AFTER_DELIVERY = 'returned_after_delivery'
    DEFERRED = 'deferred'
    # Add more status options as needed

    STATUS_CHOICES = [
        (PENDING, 'طلبات معلقة'),
        (PREPARATION, 'طلبات جاري التحضير'),
        (SHIPPED, 'طلبات تم الشحن'),
        (DELIVERED, 'طلبات تم التوصيل'),
        (RETURN_IN_PROGRESS, 'جار الاسترجاع'),
        (CANCELED, 'طلبات ملغيه'),
        (POST_DELIVERY_RETURN, 'طلبات مرتجعة'),
        (RETURNED, 'طلبات مرتجعة بعد التسليم'),
        (RETURNED_AFTER_DELIVERY, 'طلبات مرتجعة بعد التوصيل'),
        (DEFERRED, 'طلبات مؤجله'),
        # Add more choices as needed
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=PENDING)
    barcode = models.CharField(max_length=10, unique=True, default=generate_unique_barcode)
    barcode_returned = models.CharField(max_length=11, unique=False, default=generate_unique_barcode_returned)
    marketer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='marketer_orders', limit_choices_to={'is_marketer': True})
    client_name = models.CharField(max_length=255)
    client_phone1 = models.CharField(max_length=255)
    client_phone2 = models.CharField(max_length=255)
    client_address = models.TextField()
    governorate = models.ForeignKey(ShippingPrice, on_delete=models.CASCADE)
    # city = models.ForeignKey(City, on_delete=models.CASCADE)
    city = ChainedForeignKey(
        City,
        chained_field="governorate",
        chained_model_field="governorate",
        show_all=False,
        auto_choose=True,
        sort=True,
    )
    shiping_price = models.IntegerField(default=0)
    shipping_company = models.ForeignKey(ShippingCompany, on_delete=models.SET_NULL, null=True, blank=True)
    commission = models.IntegerField(default=0)
    # products = models.ManyToManyField(Product, through='OrderItem', related_name='order_items')
    total = models.IntegerField()
    total_items_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Adjust max_digits and decimal_places as needed

    note = models.TextField()
    whats1_clicked = models.IntegerField(default=0)
    phone1_clicked = models.IntegerField(default=0)
    sms1_clicked = models.IntegerField(default=0)
    whats2_clicked = models.IntegerField(default=0)
    phone2_clicked = models.IntegerField(default=0)
    sms2_clicked = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.barcode} x {self.status} ({self.governorate})"

    def get_total_items_price(self):
        total = 0
        for item in self.items.all():
            total += item.get_total_item_price()
        return total
    

    def get_shipping_price(self):
        price = self.governorate.price
        return price
    

    def get_commission(self):
        price = self.total - (self.total_items_price + self.shiping_price)
        return price
    
    
    def update_click_counters(self, action_type):
        if action_type == 'whats1':
            self.whats1_clicked += 1
            print(self.whats1_clicked)
        elif action_type == 'phone1':
            self.phone1_clicked += 1
        elif action_type == 'sms1':
            self.sms1_clicked += 1
        elif action_type == 'whats2':
            self.whats2_clicked += 1
        elif action_type == 'phone2':
            self.phone2_clicked += 1
        elif action_type == 'sms2':
            self.sms2_clicked += 1

        self.save()

 
    def save(self, *args, **kwargs):
        # Update the total_items_price before saving
        self.total_items_price = self.get_total_items_price()
        self.shiping_price = self.get_shipping_price()
        self.commission = self.get_commission()

        super().save(*args, **kwargs)

        # If the order is delivered, update the marketer's profit
        if self.status == self.DELIVERED and self.marketer:
            self.marketer.profit += self.get_commission()
            self.marketer.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_variants')
    quantity = models.PositiveIntegerField()    
    total_item_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} x ({self.variant})  in Order #{self.order.barcode}"

    def get_total_item_price(self):
        price = self.quantity * self.product.sale_price
        return price
    
    def get_vendor_profit(self):
        profit = self.quantity * self.product.purchase_price
        return profit
            
    def get_admin_profit(self):
        profit = self.quantity * (self.product.sale_price - self.product.purchase_price)
        return profit
    

    def save(self, *args, **kwargs):
        # Update the total_item_price before saving
        self.total_item_price = self.get_total_item_price()
        super().save(*args, **kwargs)