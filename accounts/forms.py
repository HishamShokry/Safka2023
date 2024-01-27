from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import *


class SignInForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "البريد الأكتروني"}
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "كلمة السر"}
        )
    )


class SignUpFormMarketer(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "الأسم الأول"}
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "الأسم الثاني"}
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "البريد الأكتروني"}
        )
    )

    mobile_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "رقم الهاتف (e.g. 01012345678)",
            }
        ),
        validators=[
            RegexValidator(
                regex=r'^01[0-9]{9}$',
                message="الرقم يجب أن يكون بصيغة صحيحة (مثال: 01012345678)",
                code="invalid_mobile_number",
            )
        ]
    )

    facebook_page_url = forms.CharField(
        widget=forms.URLInput(
            attrs={"class": "form-control", "placeholder": "اسم صفحة الفيسبوك"}
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "كلمة السر"}
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "تأكيد كلمة السر"}
        )
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
            "is_marketer",
            "first_name",
            "last_name",
            "facebook_page_url",
            "mobile_number"

        )





class SignUpFormVendor(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "الأسم الأول"}
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "الأسم الثاني"}
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "البريد الأكتروني"}
        )
    )

    mobile_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "رقم الهاتف (e.g. 01012345678)",
            }
        ),
        validators=[
            RegexValidator(
                regex=r'^01[0-9]{9}$',
                message="الرقم يجب أن يكون بصيغة صحيحة (مثال: 01012345678)",
                code="invalid_mobile_number",
            ),
        ]
    )

    store_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "اسم المتجر "}
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "كلمة السر"}
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "تأكيد كلمة السر"}
        )
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
            "is_vendor",
            "first_name",
            "last_name",
            "store_name",
            "mobile_number"

        )




class ChangeProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('profile_photo',)