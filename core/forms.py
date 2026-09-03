from django import forms

from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)

from .models import User, Product, Order

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User

        fields = (
            "email",
            "full_name",
            "village_town_city",
            "state",
            "pincode",
            "user_type",
        )

        widgets = {
            "email": forms.EmailInput(attrs={
                "placeholder": "Enter your email address"
            }),

            "full_name": forms.TextInput(attrs={
                "placeholder": "Enter your full name"
            }),

            "village_town_city": forms.TextInput(attrs={
                "placeholder": "Village / Town / City"
            }),

            "state": forms.TextInput(attrs={
                "placeholder": "Enter your state"
            }),

            "pincode": forms.TextInput(attrs={
                "placeholder": "Enter your pincode",
                "maxlength": "10"
            }),

            "user_type": forms.RadioSelect(),
        }


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User

        fields = (
            "email",
            "full_name",
            "village_town_city",
            "state",
            "pincode",
            "user_type",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )


# ==========================================================
# FarmPro Product Form
# ==========================================================

# =========================================================
# PRODUCT FORM
# =========================================================

class ProductForm(forms.ModelForm):

    class Meta:

        model = Product

        fields = (
            "name",
            "category",
            "image",
            "price",
            "quantity",
            "unit",
            "location",
        )

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "placeholder": "Enter product name",
                    "class": "w-full px-4 py-3 rounded-xl border border-black/10 outline-none"
                }
            ),

            "category": forms.TextInput(
                attrs={
                    "placeholder": "Example: Rice, Wheat, Dal, Vegetable",
                    "class": "w-full px-4 py-3 rounded-xl border border-black/10 outline-none"
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "accept": "image/*",
                    "class": "hidden"
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "placeholder": "Enter price",
                    "step": "0.01",
                    "class": "w-full px-4 py-3 rounded-xl border border-black/10 outline-none"
                }
            ),

            "quantity": forms.NumberInput(
                attrs={
                    "placeholder": "Enter quantity",
                    "step": "0.01",
                    "class": "w-full px-4 py-3 rounded-xl border border-black/10 outline-none"
                }
            ),

            "unit": forms.Select(
                attrs={
                    "class": "w-full px-4 py-3 rounded-xl border border-black/10 outline-none"
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "placeholder": "Enter product location",
                    "class": "w-full px-4 py-3 rounded-xl border border-black/10 outline-none"
                }
            ),
        }
# =========================================================
# PROFILE FORM
# =========================================================
class ProfileForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            "full_name",
            "email",
            "village_town_city",
            "state",
            "pincode",
            "upi_id",
        ]

        widgets = {

            "upi_id": forms.TextInput(
                attrs={
                    "placeholder": "example@upi",
                    "class": "w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-[#1A2E22]"
                }
            ),

        }
# =========================================================
# ORDER FORM
# =========================================================

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order

        fields = (
            "quantity",
        )

        widgets = {
            "quantity": forms.NumberInput(
                attrs={
                    "placeholder": "Enter quantity",
                    "min": "0.01",
                    "step": "0.01",
                }
            ),
        }