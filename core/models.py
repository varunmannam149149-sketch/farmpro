from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# =========================================================
# CUSTOM USER MANAGER
# =========================================================

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(
            email,
            password,
            **extra_fields
        )


# =========================================================
# FARMPro USER
# =========================================================

class User(AbstractUser):

    username = None

    PRODUCER = "producer"
    CONSUMER = "consumer"
    MARKET = "market"

    USER_TYPE_CHOICES = [
        (PRODUCER, "Producer"),
        (CONSUMER, "Consumer"),
        (MARKET, "Market"),
    ]

    full_name = models.CharField(
        max_length=150
    )

    email = models.EmailField(
        unique=True
    )

    village_town_city = models.CharField(
        max_length=150
    )

    state = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    # Producer UPI ID
    upi_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.full_name


# =========================================================
# FARMPro PRODUCT
# =========================================================

class Product(models.Model):

    UNIT_CHOICES = [
        ("kg", "Kilogram"),
        ("quintal", "Quintal"),
        ("ton", "Ton"),
    ]

    producer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={
            "user_type": "producer"
        },
        related_name="products"
    )

    name = models.CharField(
        max_length=100
    )

    category = models.CharField(
        max_length=100
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES
    )

    location = models.CharField(
        max_length=200
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


# =========================================================
# FARMPro ORDER
# =========================================================

class Order(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    CANCELLED_BY_CHOICES = (
        ("producer", "Producer"),
        ("consumer", "Consumer"),
        ("market", "Market / Shop"),
    )

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    cancelled_by = models.CharField(
        max_length=20,
        choices=CANCELLED_BY_CHOICES,
        blank=True,
        null=True
    )

    cancellation_reason = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.product.name}"



#subsricber 
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

#contact informaion 
class ContactMessage(models.Model):
    USER_TYPES = [
        ('producer', 'Producer'),
        ('market', 'Market'),
        ('consumer', 'Consumer'),
        ('partner', 'Business / Partner'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='other')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    

"""
# # =========================================================
# # FARMPro PAYMENT
# # =========================================================

# class Payment(models.Model):

    PAYMENT_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    )

    PAYMENT_METHOD_CHOICES = (
        ("upi", "UPI"),
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="upi"
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending"
    )

    transaction_id = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Payment for Order #{self.order.id}"

        """