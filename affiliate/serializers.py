import json
import re
from rest_framework import serializers
from .models import *
from django.contrib.auth.decorators import login_required
from accounts.decorators import *


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"

    def validate_name(self, value):
        instance = self.instance

        if instance is not None and instance.name.lower() == value.lower():
            return value  # No change in the name, validation passed

        existing_inventory = Inventory.objects.filter(name__iexact=value).first()

        if existing_inventory:
            raise serializers.ValidationError("يوجد مخزون بهذا الاسم بالفعل.")

        return value

    # def validate(self, data):
    #     user = self.context['request'].user
    #     # Check if the user is an admin
    #     if user.is_authenticated and (user.is_admin or user.is_superuser or user.is_impersonate):
    #         return data

    #     else:
    #         raise serializers.ValidationError("You do not have permission to perform this action.")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def validate_name(self, value):
        existing_category = (
            Category.objects.filter(name__iexact=value)
            .exclude(id=self.instance.id if self.instance else None)
            .first()
        )

        if existing_category:
            raise serializers.ValidationError("هناك فئة بهذا الاسم موجودة بالفعل.")

        return value


class ShippingCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingCompany
        fields = "__all__"

    def validate_name(self, value):
        existing_inventory = (
            ShippingCompany.objects.filter(name__iexact=value)
            .exclude(id=self.instance.id if self.instance else None)
            .first()
        )

        if existing_inventory:
            raise serializers.ValidationError("توجد شركة شحن بهذا الاسم بالفعل.")

        return value


class ShippingPriceSerializer(serializers.ModelSerializer):
    governorate_name = serializers.ReadOnlyField(
        source="governorate.governorate_name_ar"
    )

    class Meta:
        model = ShippingPrice
        fields = [
            "id",
            "governorate",
            "governorate_name",
            "price",
            "is_active",
            "created_at",
            "updated_at",
        ]

    def validate_price(self, value):
        """
        Validate that the price is a positive integer.
        """
        if value <= 0 or type(value) is not int:
            raise serializers.ValidationError("يجب أن يكون السعر عددًا صحيحًا موجبًا.")
        return value

    def validate_governorate(self, value):
        """
        Validate that the governorate is not None and not duplicated.
        """
        existing_governorate = (
            ShippingPrice.objects.filter(governorate__exact=value)
            .exclude(id=self.instance.id if self.instance else None)
            .first()
        )

        if existing_governorate:
            raise serializers.ValidationError("محافظة بهذا الاسم موجودة بالفعل.")

        if value is None:
            raise serializers.ValidationError("لا يمكن أن تكون المحافظة فارغة.")
        return value


class GovernorateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Governorate
        fields = "__all__"


class ProductVariantSerializer(serializers.ModelSerializer):
    size_name = serializers.StringRelatedField(source="size")
    color_name = serializers.StringRelatedField(source="color")
    color_hex = serializers.StringRelatedField(source="color.color")
    product_name = serializers.StringRelatedField(source="product")
    sale_price = serializers.StringRelatedField(source="product.sale_price")
    

    class Meta:
        model = ProductVariant
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    product_variant_set = ProductVariantSerializer(many=True, read_only=True)
    # product_variant_set_str = serializers.CharField(write_only = True)
    # access_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    # access_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    category_name = serializers.StringRelatedField(source="category")
    inventory_name = serializers.StringRelatedField(source="inventory")
    vendor_name = serializers.StringRelatedField(source="vendor")
    access_to_name = serializers.StringRelatedField(
        many=True, read_only=True, source="access_to"
    )

    class Meta:
        model = Product
        fields = '__all__'
        # fields = [
        #     'id',
        #     'product_variant_set',
        #     'category_name',
        #     'inventory_name',
        #     'vendor_name',
        #     'access_to_name',
        #     'inventory',
        #     'vendor',
        #     'category',
        #     'access_to',
        #     'name',
        #     'purchase_price',
        #     'sale_price',
        #     'image',
        #     'description',
        #     'note',
        #     'media_url',
        #     'is_active',
        #     'access_type',
        #     'barcode',
        #     'created_at',
        #     'updated_at',
        #     # 'product_variant_set_str',
        # ]


    def validate_purchase_price(self, value):
        """
        Validate that purchase_price is greater than zero.
        """
        if value <= 0:
            raise serializers.ValidationError("يجب أن يكون سعر الشراء أكبر من الصفر.")
        return value

    def validate_sale_price(self, value):
        """
        Validate that sale_price is greater than zero.
        """
        if value <= 0:
            raise serializers.ValidationError("يجب أن يكون سعر البيع أكبر من الصفر.")
        return value

    def validate_size(self, value):
        """
        Validate that size is one of the predefined choices.
        """
        valid_sizes = [choice[0] for choice in Product.sizes_choices]
        if value not in valid_sizes:
            raise serializers.ValidationError("اختيار الحجم غير صالح.")
        return value

    def validate_name(self, value):
        """
        Validate that the name is not empty and is unique among products.
        """
        if not value.strip():
            raise serializers.ValidationError("لا يمكن أن يكون الاسم فارغًا.")

        # If the instance exists, exclude it from the uniqueness check
        instance = getattr(self, "instance", None)
        if (
            instance
            and Product.objects.filter(name__iexact=value)
            .exclude(pk=instance.pk)
            .exists()
        ):
            raise serializers.ValidationError("يوجد منتج بهذا الاسم بالفعل.")

        # For new instances, check for uniqueness among all products
        if not instance and Product.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("يوجد منتج بهذا الاسم بالفعل.")

        return value

    def validate_image(self, value):
        """
        Validate that the image is not too large.
        """
        max_size = 5 * 1024 * 1024  # 5 MB
        if value.size > max_size:
            raise serializers.ValidationError(
                "يجب أن يكون حجم الصورة أقل من 5 ميغابايت."
            )
        return value

    def validate_description(self, value):
        """
        Validate that the description is not too short.
        """
        min_length = 10
        if len(value.strip()) < min_length:
            raise serializers.ValidationError(
                f"يجب أن يبلغ طول الوصف {min_length} من الأحرف على الأقل."
            )
        return value

    def validate_product_variant_set(self, value):
            if not value:
                raise serializers.ValidationError("Product variant set cannot be empty.")
            return value



class OrderItemSerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True)
    variant = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all())
    variant_details = ProductVariantSerializer(source="variant", read_only=True)
    class Meta:
        model = OrderItem
        # fields = ("product", "order", "quantity", "total_item_price")
        fields = '__all__'



    def validate_quantity(self, value):
        """
        Validate the 'quantity' field.
        """
        if value <= 0:
            raise serializers.ValidationError("يجب ان تكون الكمية قيمة اكبر من 0.")
        return value
    


class OrderHistorySerializer(serializers.ModelSerializer):
    history_entries = serializers.SerializerMethodField()

    class Meta:
        model = OrderHistory
        fields = '__all__'

    def get_history_entries(self, obj):
        # Retrieve the related history entries for the current OrderHistory instance
        entries = OrderSerializer(obj.history_entries.all(), many=True).data
        return entries
    


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    marketer_name = serializers.StringRelatedField(source="marketer")
    governorate_name = serializers.StringRelatedField(source="governorate")
    city_name = serializers.StringRelatedField(source="city")
    shipping_company_name = serializers.StringRelatedField(source="shipping_company")
    # history_entries = OrderHistorySerializer(many=True, read_only=True)  # Include history entries
    class Meta:
        model = Order
        fields = '__all__'
    
    def validate_total(self, value):
        """
        Validate the 'total' field.
        """
        if value <= 0:
            raise serializers.ValidationError("يجب أن يكون الإجمالي قيمة غير سالبة.")
        return value
    

    def validate_commission(self, value):
        """
        Validate the 'commission' field.
        """
        if value < 30:
            raise serializers.ValidationError("يجب أن تكون العمولة اكثر من 30 جنيه.")
        return value
    
    def validate_client_name(self, value):
        """
        Validate the 'client_name' field.
        """

        if len(value) < 1:  # Check if the string is empty or contains only whitespace
            raise serializers.ValidationError("يجب ادخال اسم العميل.")
        return value
    
    def validate_client_phone1(self, value):
        """
        Validate the 'client_phone1' field to be in the format '01XXXXXXXXX'.
        """
        phone_pattern = re.compile(r'^01\d{9}$')

        if not phone_pattern.match(value):
            raise serializers.ValidationError("تنسيق رقم الهاتف غير صالح. ينبغي أن يكون مثل '01XXXXXXXXX'.")

        return value
    
    def validate_client_phone2(self, value):
        """
        Validate the 'client_phone2' field to be in the format '01XXXXXXXXX'.
        """
        phone_pattern = re.compile(r'^01\d{9}$')

        if not phone_pattern.match(value):
            raise serializers.ValidationError("تنسيق رقم الهاتف غير صالح. ينبغي أن يكون مثل '01XXXXXXXXX'.")

        return value
    



    def validate(self, data):
        client_name = data.get('client_name')
        client_phone1 = data.get('client_phone1')


        existing_orders = Order.objects.filter(
            client_name=client_name,
            client_phone1=client_phone1,
        )


        # If an order already exists, raise a validation error
        if self.instance:
            existing_orders = existing_orders.exclude(pk=self.instance.pk)

        if existing_orders.exists():
            raise serializers.ValidationError("يوجد طلب بنفس معلومات العميل بالفعل.")
        

        # Check if the client_name is an empty string or contains only whitespace characters
        if not client_name.strip():
            raise serializers.ValidationError("يجب ادخال اسم العميل.")

        return data
    


