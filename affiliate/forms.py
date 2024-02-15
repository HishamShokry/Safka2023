from django import forms
from .models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = False
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "ادخل اسم القسم هنا"}
        )

        # self.fields['inventory'].label = 'اختر المخزن'
        # self.fields["inventory"].widget.attrs.update({"class": "select2"})

    class Meta:
        model = Category
        fields = ["name"]
        # fields = ["name", "inventory"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        # }
        # Optionally, you can exclude some fields if needed
        # exclude = ['created_at', 'updated_at']

    def clean_name(self):
        # Example custom validation for the 'name' field
        name = self.cleaned_data["name"]
        # Add your custom validation logic here if needed
        return name


class InventoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = False
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "ادخل اسم المخزن هنا"}
        )

        # self.fields['inventory'].label = 'اختر المخزن'
        # self.fields["inventory"].widget.attrs.update({"class": "select2"})

    class Meta:
        model = Inventory
        fields = ["name"]
        # fields = ["name", "inventory"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        # }
        # Optionally, you can exclude some fields if needed
        # exclude = ['created_at', 'updated_at']

    def clean_name(self):
        # Example custom validation for the 'name' field
        name = self.cleaned_data["name"]
        # Add your custom validation logic here if needed
        return name


class ShippingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = False
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "ادخل اسم المخزن هنا"}
        )

        self.fields["website"].label = False
        self.fields["website"].widget.attrs.update(
            {"class": "form-control", "placeholder": "ادخل رابط الموقع هنا"}
        )

    class Meta:
        model = ShippingCompany
        fields = ["name", "website"]
        # fields = ["name", "inventory"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        # }
        # Optionally, you can exclude some fields if needed
        # exclude = ['created_at', 'updated_at']

    def clean_name(self):
        # Example custom validation for the 'name' field
        name = self.cleaned_data["name"]
        # Add your custom validation logic here if needed
        return name

    def clean_website(self):
        # Example custom validation for the 'website' field
        website = self.cleaned_data["website"]
        # Add your custom validation logic here if needed
        return website


class ShippingPriceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["governorate"].label = "المحافظة"
        self.fields["governorate"].widget.attrs.update(
            {"class": "form-control select2"}
        )

        self.fields["price"].label = False
        self.fields["price"].widget.attrs.update(
            {"class": "form-control", "placeholder": "ادخل سعر الشحن هنا"}
        )

        self.fields["is_active"].label = "نشط"
        self.fields["is_active"].widget.attrs.update({"class": ""})

    class Meta:
        model = ShippingPrice
        fields = ["governorate", "price", "is_active"]
        # fields = ["name", "inventory"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        # }
        # Optionally, you can exclude some fields if needed
        # exclude = ['created_at', 'updated_at']


class ProductVariantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["size"].label = "مقاس"
        self.fields["size"].widget.attrs.update({"class": "form-control select2"})

        self.fields["color"].label = "اللون"
        self.fields["color"].widget.attrs.update({"class": "form-control select2"})

        self.fields["quantity"].label = "الكمية"
        self.fields["quantity"].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = ProductVariant
        fields = ["size", "color", "quantity"]


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields["barcode"].label = 'كود'
        # self.fields["barcode"].widget.attrs.update(
        #     {"class": "form-control"}
        # )
        # self.fields['barcode'].widget.attrs['readonly'] = True

        self.fields["name"].label = False
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "أسم المنتج"}
        )

        self.fields["purchase_price"].label = False
        self.fields["purchase_price"].widget.attrs.update(
            {"class": "form-control", "placeholder": "سعر الشراء"}
        )

        self.fields["sale_price"].label = False
        self.fields["sale_price"].widget.attrs.update(
            {"class": "form-control", "placeholder": "سعر البيع"}
        )

        self.fields["image"].label = False
        self.fields["image"].widget.attrs.update(
            {"class": "form-control", "placeholder": "صورة المنتج "}
        )

        # self.fields["size"].label = 'مقاس'
        # self.fields["size"].widget.attrs.update(
        #     {"class": "form-control select2"}
        # )

        self.fields["description"].label = False
        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "وصف المنتج ..."}
        )

        self.fields["note"].label = False
        self.fields["note"].widget.attrs.update(
            {"class": "form-control", "placeholder": "ملاحظة للمنتج ..."}
        )

        self.fields["media_url"].label = False
        self.fields["media_url"].widget.attrs.update(
            {"class": "form-control", "placeholder": "رابط الصور"}
        )

        self.fields["is_active"].label = "نشط"
        self.fields["is_active"].widget.attrs.update({"class": ""})

        self.fields["inventory"].label = "المخزن"
        self.fields["inventory"].widget.attrs.update({"class": "form-control select2"})

        self.fields["vendor"].label = "التاجر"
        self.fields["vendor"].widget.attrs.update({"class": "form-control select2"})

        self.fields["category"].label = "القسم"
        self.fields["category"].widget.attrs.update({"class": "form-control select2"})

        self.fields["access_type"].label = "الخصوصية"
        self.fields["access_type"].widget.attrs.update(
            {"class": "form-control select2"}
        )

        self.fields["access_to"].label = "متاح لمن"
        self.fields["access_to"].widget.attrs.update({"class": "form-control select2"})

    product_variant_set = forms.inlineformset_factory(
        Product,
        ProductVariant,
        form=ProductVariantForm,
        extra=1,
        can_delete=True,
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "inventory",
            "vendor",
            "purchase_price",
            "sale_price",
            "image",
            "media_url",
            "description",
            "note",
            "access_type",
            "access_to",
            "is_active",
        ]

    def clean_purchase_price(self):
        purchase_price = self.cleaned_data["purchase_price"]
        if purchase_price < 0:
            raise forms.ValidationError("يجب أن يكون سعر الشراء قيمة غير سالبة.")
        return purchase_price

    def clean_sale_price(self):
        sale_price = self.cleaned_data["sale_price"]
        if sale_price < 0:
            raise forms.ValidationError("يجب أن يكون سعر البيع قيمة غير سالبة.")
        return sale_price

    def clean_name(self):
        name = self.cleaned_data["name"]
        if not name or len(name) > 255:
            raise forms.ValidationError("الاسم مطلوب ويجب ألا يزيد عن 255 حرفًا.")
        return name

    # def clean_image(self):
    #     image = self.cleaned_data['image']
    #     if image:
    #         # Add custom validation for image file types or size if needed
    #         pass
    #     return image

    # def clean_size(self):
    #     size = self.cleaned_data['size']
    #     if size and size not in dict(Product.sizes_choices).keys():
    #         raise forms.ValidationError("تحديد الحجم غير صالح.")
    #     return size

    def clean_description(self):
        description = self.cleaned_data["description"]
        # Add custom validation for the description field if needed
        return description

    def clean_note(self):
        note = self.cleaned_data["note"]
        # Add custom validation for the note field if needed
        return note

    def clean_media_url(self):
        media_url = self.cleaned_data["media_url"]
        # Add custom validation for the media_url field if needed
        return media_url

    def clean_access_type(self):
        access_type = self.cleaned_data["access_type"]
        if access_type not in ["public", "private"]:
            raise forms.ValidationError("نوع الوصول غير صالح.")
        return access_type

    def clean(self):
        cleaned_data = super().clean()
        # Add any custom validation that involves multiple fields here
        return cleaned_data


class OrderItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["product"].queryset = Product.objects.all()

        # if "product" in self.data:
        #     # If there is data for the "product" field, update the queryset based on the search term
        #     term = self.data.get("product")
        #     self.fields["product"].queryset = Product.objects.filter(
        #         name__icontains=term
        #     )
        # elif self.instance.pk:
        #     # If the instance already exists, filter the queryset based on the product of the instance
        #     self.fields["product"].queryset = Product.objects.filter(
        #         pk=self.instance.product.pk
        #     )

        self.fields["product"].label = "المنتج"
        self.fields["product"].widget.attrs.update(
            {"class": "form-control select2 product-select "}
        )
        self.fields["variant"].label = "الخاصية"
        self.fields["variant"].widget.attrs.update(
            {"class": "form-control select2 variant-select"}
        )
        self.fields["quantity"].label = False
        self.fields["quantity"].widget.attrs.update(
            {"class": "form-control quantity-input", "placeholder": "الكمية"}
        )
        self.fields["total_item_price"].label = False
        self.fields["total_item_price"].widget.attrs.update(
            {
                "class": "form-control total-item-price",
                "placeholder": "اجمالي سعر الطلب",
            }
        )

    class Meta:
        model = OrderItem
        fields = "__all__"  # Use all fields from the OrderItem model


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Set default marketer to the logged-in user
        if user and user.is_authenticated:
            self.fields["marketer"].initial = user

        # self.fields["status"].label = "الحالة"
        # self.fields["status"].widget.attrs.update(
        #     {"class": "form-control select2", "disabled": "disabled"}
        # )
        self.fields["marketer"].label = "المسوق"
        self.fields["marketer"].widget.attrs.update({"class": "form-control select2"})
        self.fields["client_name"].label = False
        self.fields["client_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "اسم العميل"}
        )
        self.fields["client_phone1"].label = False
        self.fields["client_phone1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "1 رقم العميل"}
        )
        self.fields["client_phone2"].label = False
        self.fields["client_phone2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "2 رقم العميل"}
        )
        self.fields["client_address"].label = False
        self.fields["client_address"].widget.attrs.update(
            {"class": "form-control", "placeholder": "عنوان العميل"}
        )

        self.fields["city"].label = "المدينة"
        self.fields["city"].widget.attrs.update({"class": "form-control select2 cities"})
        self.fields["governorate"].label = "المحافظة"
        self.fields["governorate"].widget.attrs.update(
            {"class": "form-control governorates select2"}
        )
        self.fields["shiping_price"].label = "سعر الشحن"
        self.fields["shiping_price"].widget.attrs.update(
            {"class": "form-control select2",
             "disabled": "disabled"}
        )
        self.fields["shipping_company"].label = "شركة الشحن"
        self.fields["shipping_company"].widget.attrs.update(
            {"class": "form-control select2"}
        )
        self.fields["total"].label = "الاجمالي"
        self.fields["total"].widget.attrs.update({"class": "form-control"})
        self.fields["note"].label = "ملاحظة"
        self.fields["note"].widget.attrs.update({"class": "form-control"})

    items = forms.inlineformset_factory(
        Order,
        OrderItem,
        form=OrderItemForm,
        extra=1,
        can_delete=True,
    )

    def get_valid_status_choices(self):
        instance = self.instance
        if instance.status == Order.PENDING:
            return [Order.CANCELED, Order.POSTPONED]
        elif instance.status == Order.PREPARATION:
            return [Order.CANCELED_DURING_PREPARATION, Order.SHIPPED]
        elif instance.status == Order.SHIPPED:
            return [Order.DELIVERED, Order.RETURN_IN_PROGRESS]
        elif instance.status == Order.RETURN_IN_PROGRESS:
            return [Order.RETURNED]
        elif instance.status == Order.DELIVERED:
            return [Order.RETURNE_REQUESTS]
        elif instance.status == Order.RETURNE_REQUESTS:
            return [Order.RETURNED]
        else:
            return []

    class Meta:
        model = Order
        fields = [
            # "status",
            "marketer",
            "client_name",
            "client_phone1",
            "client_phone2",
            "client_address",
            "governorate",
            "city",
            "shiping_price",
            "shipping_company",
            "total",
            "note",
        ]  # Use all fields from the Order model

    # You can add additional customization for form fields or validation here if needed
    def clean_total(self):
        total = self.cleaned_data.get('total')

        # Add your custom validation logic for the 'total' field
        if total < 0:
            raise ValidationError(_('Total must be a non-negative value.'))

        return total   
    
    def clean(self):
        cleaned_data = super().clean()
        shiping_price = cleaned_data.get('shiping_price')
        total = cleaned_data.get('total')

        # Add cross-field validation logic
        if shiping_price and total and shiping_price > total:
            raise ValidationError(_('Shipping price cannot exceed the total.'))

        return cleaned_data
    





class OrderFormMarketer(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["client_name"].label = False
        self.fields["client_name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "اسم العميل"}
        )

        self.fields["client_phone1"].label = False
        self.fields["client_phone1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "1 رقم العميل"}
        )
        self.fields["client_phone2"].label = False
        self.fields["client_phone2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "2 رقم العميل"}
        )
        self.fields["client_address"].label = False
        self.fields["client_address"].widget.attrs.update(
            {"class": "form-control", "placeholder": "عنوان العميل"}
        )

        self.fields["city"].label = "المدينة"
        self.fields["city"].widget.attrs.update({"class": "form-control select2 cities"})
        self.fields["governorate"].label = "المحافظة"
        self.fields["governorate"].widget.attrs.update(
            {"class": "form-control governorates select2"}
        )
        self.fields["shiping_price"].label = "سعر الشحن"
        self.fields["shiping_price"].widget.attrs.update(
            {"class": "form-control select2",
             "disabled": "disabled"}
        )

        self.fields["total"].label = "الاجمالي"
        self.fields["total"].widget.attrs.update({"class": "form-control"})
        self.fields["note"].label = "ملاحظة"
        self.fields["note"].widget.attrs.update({"class": "form-control"})

    items = forms.inlineformset_factory(
        Order,
        OrderItem,
        form=OrderItemForm,
        extra=1,
        can_delete=True,
    )

    def get_valid_status_choices(self):
        instance = self.instance
        if instance.status == Order.PENDING:
            return [Order.CANCELED, Order.POSTPONED]
        elif instance.status == Order.PREPARATION:
            return [Order.CANCELED_DURING_PREPARATION, Order.SHIPPED]
        elif instance.status == Order.SHIPPED:
            return [Order.DELIVERED, Order.RETURN_IN_PROGRESS]
        elif instance.status == Order.RETURN_IN_PROGRESS:
            return [Order.RETURNED]
        elif instance.status == Order.DELIVERED:
            return [Order.RETURNE_REQUESTS]
        elif instance.status == Order.RETURNE_REQUESTS:
            return [Order.RETURNED]
        else:
            return []

    class Meta:
        model = Order
        fields = [
            # "status",
            "client_name",
            "client_phone1",
            "client_phone2",
            "client_address",
            "governorate",
            "city",
            "shiping_price",
            "total",
            "note",
        ]  # Use all fields from the Order model

    # You can add additional customization for form fields or validation here if needed
    def clean_total(self):
        total = self.cleaned_data.get('total')

        # Add your custom validation logic for the 'total' field
        if total < 0:
            raise ValidationError(_('Total must be a non-negative value.'))

        return total   
    
    def clean(self):
        cleaned_data = super().clean()
        shiping_price = cleaned_data.get('shiping_price')
        total = cleaned_data.get('total')

        # Add cross-field validation logic
        if shiping_price and total and shiping_price > total:
            raise ValidationError(_('Shipping price cannot exceed the total.'))

        return cleaned_data
    


class RequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["amount"].label = False
        self.fields["amount"].widget.attrs.update(
            {"class": "form-control", "placeholder": "القيمة"}
        )

        self.fields["payment_method"].label = False
        self.fields["payment_method"].widget.attrs.update(
            {"class": "form-control", "placeholder": "طريقة الدفع"}
        )


        self.fields["vodafone_field"].label = False
        self.fields["vodafone_field"].widget.attrs.update(
            {"class": "form-control", "placeholder": "فودافون كاش"}
        )

        self.fields["instapay_field"].label = False
        self.fields["instapay_field"].widget.attrs.update(
            {"class": "form-control", "placeholder": "انستا باي"}
        )

        self.fields["bank_field"].label = False
        self.fields["bank_field"].widget.attrs.update(
            {"class": "form-control", "placeholder": "تحويل بنكي"}
        )

        self.fields["note"].label = False
        self.fields["note"].widget.attrs.update(
            {"class": "form-control", "placeholder": "ملاحظة"}
        )

        
    class Meta:
        model = Request
        fields = ["amount", "payment_method", 'vodafone_field', 'instapay_field', 'bank_field', 'note']