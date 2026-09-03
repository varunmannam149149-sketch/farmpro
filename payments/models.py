from django.db import models


class Payment(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]

    order = models.OneToOneField(
        "core.Order",
        on_delete=models.CASCADE,
        related_name="farmpro_payment"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    producer_upi_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    qr_code = models.ImageField(
        upload_to="payment_qr/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
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


from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


