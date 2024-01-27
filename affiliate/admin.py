from django.contrib import admin
from .models import *
from django.forms import Textarea 
from django.utils.html import format_html
from django import forms
# Register your models here.



class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1  # Number of empty forms to display for adding variants inline


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('barcode',)
    list_display = ("name", 'barcode', "sale_price", "is_active", "created_at", "updated_at")
    list_filter = ("category", "is_active", "vendor", 'inventory', 'name')
    ordering = ("-created_at",)
    # raw_id_fields = ("category", "inventory", "vendor", "access_to")
    autocomplete_fields = ['access_to', 'vendor',]

    formfield_overrides = {
            models.JSONField: {'widget': Textarea(attrs={'rows': 2, 'cols': 40})},
        }
    
    inlines = [ProductVariantInline]


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


class CityAdmin(admin.ModelAdmin):
    search_fields = ['city_name_ar']



class ColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'display_color']

    def display_color(self, obj):
        return format_html('<div style="width: 20px; height: 20px; background-color: {};"></div>', obj.color)

    display_color.short_description = 'Color Preview'





class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Number of empty forms to display for adding order items inline
    # readonly_fields = ['total_price_display']  # Add the readonly field for total price
    # template = 'admin/orderitem_inline.html'  # Custom template to include JavaScript
    
    # def total_price_display(self, obj):
    #     return obj.total_price()
        
    # total_price_display.short_description = 'Total Price'





class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['id', 'barcode', 'marketer', 'client_name', 'client_phone1', 'commission' ,'shiping_price','total', 'status', 'created_at', 'updated_at',]
    list_filter = ['status', 'marketer', 'created_at', 'shipping_company',]
    search_fields = ['client_name', 'client_phone1', 'client_phone2', 'barcode']

    readonly_fields = ('total_items_price', 'shiping_price', 'commission')

    # def display_total_order_price(self, obj):
    #     return obj.get_total_items_price()
    
    # display_total_order_price.short_description = 'Total Order Price'

    # def get_shipping_cost(self, obj):
    #     # Custom method to dynamically calculate and display shipping cost
    #     return obj.shipping  # Assumes you've already added the shipping property to your Order model

    


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Inventory)
admin.site.register(ShippingCompany)
admin.site.register(Governorate)
admin.site.register(City, CityAdmin)
admin.site.register(ShippingPrice)
admin.site.register(Order, OrderAdmin)
admin.site.register(Size)
admin.site.register(Color, ColorAdmin)
admin.site.register(OrderItem)