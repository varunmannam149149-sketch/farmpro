from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Product
from .forms import CustomUserCreationForm, CustomUserChangeForm


from .models import ContactMessage


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User

    # Form used when creating a new user
    add_form = CustomUserCreationForm

    # Form used when editing an existing user
    form = CustomUserChangeForm

    # What we see in the Users list
    list_display = (
        "email",
        "full_name",
        "user_type",
        "village_town_city",
        "state",
        "is_active",
    )

    # Search users
    search_fields = (
        "email",
        "full_name",
        "village_town_city",
        "state",
    )

    # Ordering
    ordering = ("email",)

    # Fields shown when editing a user
    fieldsets = (
        (
            "FarmPro User Information",
            {
                "fields": (
                    "email",
                    "password",
                    "full_name",
                    "village_town_city",
                    "state",
                    "pincode",
                    "user_type",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

    # Fields shown when adding a NEW user
    add_fieldsets = (
        (
            "FarmPro User Information",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "full_name",
                    "village_town_city",
                    "state",
                    "pincode",
                    "user_type",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "price",
        "quantity",
        "unit",
        "producer",
        "location",
    )

    list_filter = (
        "category",
        "unit",
    )

    search_fields = (
        "name",
        "category",
        "location",
        "producer__full_name",
    )







from django.contrib import admin
from .models import Subscriber

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    # Columns displayed in the main table view
    list_display = ('email', 'created_at')
    
    # Enable filtering by subscription date
    list_filter = ('created_at',)
    
    # Add a search bar to quickly find specific emails
    search_fields = ('email',)
    
    # Order entries with the newest subscribers at the top
    ordering = ('-created_at',)
    
    # Set rows per page
    list_per_page = 25


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'user_type', 'subject', 'created_at')
    list_filter = ('user_type', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    