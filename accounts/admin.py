from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.utils.html import format_html
from . import models
from django import forms


User = get_user_model()


class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = "__all__"


class UserAdmin(BaseUserAdmin):
    model = models.User
    list_display = BaseUserAdmin.list_display + (
        "PENDING",
        "PREPARATION",
        "SHIPPED",
        "DELIVERED",
        "show_impersonate_link",
    )
    search_fields = ["email", "store_name"]  # Add the fields you want to search for
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Affiliate",
            {
                "fields": (
                    "is_admin",
                    "is_vendor",
                    "is_marketer",
                    "mobile_number",
                    "facebook_page_url",
                    "store_name",
                    "allow_upload_excel",
                    "profit",
                    "PENDING",
                    "PREPARATION",
                    "SHIPPED",
                    "DELIVERED",
                    "profile_photo",
                )
            },
        ),
    )
    readonly_fields = ("profit",)  # Add the readonly field(s) you want

    def show_impersonate_link(self, obj):
        url = reverse("impersonate-start", args=[obj.pk])
        redirect_url = self.get_redirect_url(obj)
        print(redirect_url)
        return format_html(
            f'<button class="btn btn-dark"><a href="{url}?next={redirect_url}">Login</a></button>'
        )

    show_impersonate_link.short_description = "Impersonate"
    form = CustomUserAdminForm  # Use the custom form for the UserAdmin

    def get_redirect_url(self, user):
        # Customize the redirection based on the user's role
        if user.is_superuser:
            return reverse('dashboard')
        elif user.is_admin:
            return reverse('dashboard')
        elif user.is_vendor:
            return reverse('vendor_dashboard')
        elif user.is_marketer:
            return reverse('marketer_dashboard')
        else:
            return reverse('/')

# admin.site.unregister(models.User)
admin.site.register(models.User, UserAdmin)
