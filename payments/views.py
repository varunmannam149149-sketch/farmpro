from io import BytesIO
from django.shortcuts import render, redirect
import qrcode

from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404, render

from core.models import Order
from .models import Payment

from django.contrib import messages
from .models import Subscriber


# =========================================================
# CHECKOUT
# =========================================================

@login_required
def checkout(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )

    # Payment is allowed only after producer confirmation
    if order.status != "confirmed":

        return render(
            request,
            "payments/failed.html",
            {
                "order": order,
                "payment": None,
                "error": "This order has not been confirmed by the producer."
            }
        )

    # -----------------------------------------------------
    # Producer
    # -----------------------------------------------------

    producer = order.product.producer

    # -----------------------------------------------------
    # Producer UPI check
    # -----------------------------------------------------

    if not producer.upi_id:

        return render(
            request,
            "payments/failed.html",
            {
                "order": order,
                "payment": None,
                "error": "The producer has not added a UPI ID."
            }
        )

    # -----------------------------------------------------
    # Get or create payment
    # -----------------------------------------------------

    payment, created = Payment.objects.get_or_create(
        order=order,
        defaults={
            "amount": order.total_price,
            "producer_upi_id": producer.upi_id,
            "status": "pending",
        }
    )

    # -----------------------------------------------------
    # Keep payment information updated
    # -----------------------------------------------------

    if payment.producer_upi_id != producer.upi_id:

        payment.producer_upi_id = producer.upi_id

        payment.save(
            update_fields=["producer_upi_id"]
        )

    # -----------------------------------------------------
    # Generate QR only if necessary
    # -----------------------------------------------------

    if not payment.qr_code:

        upi_link = (
            "upi://pay?"
            f"pa={producer.upi_id}"
            f"&pn={producer.full_name}"
            f"&am={payment.amount}"
            "&cu=INR"
        )

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4
        )

        qr.add_data(upi_link)

        qr.make(
            fit=True
        )

        qr_image = qr.make_image(
            fill_color="black",
            back_color="white"
        )

        buffer = BytesIO()

        qr_image.save(
            buffer,
            format="PNG"
        )

        payment.qr_code.save(
            f"payment_{order.id}.png",
            ContentFile(
                buffer.getvalue()
            ),
            save=True
        )

    # -----------------------------------------------------
    # UPI link
    # -----------------------------------------------------

    upi_link = (
        "upi://pay?"
        f"pa={producer.upi_id}"
        f"&pn={producer.full_name}"
        f"&am={payment.amount}"
        "&cu=INR"
    )

    # -----------------------------------------------------
    # Checkout page
    # -----------------------------------------------------

    return render(
        request,
        "payments/checkout.html",
        {
            "order": order,
            "payment": payment,
            "producer": producer,
            "upi_link": upi_link,
        }
    )


# =========================================================
# PAYMENT SUCCESS PAGE
# =========================================================

@login_required
def payment_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )

    payment = get_object_or_404(
        Payment,
        order=order
    )

    return render(
        request,
        "payments/success.html",
        {
            "order": order,
            "payment": payment,
        }
    )


# =========================================================
# PAYMENT FAILED PAGE
# =========================================================

@login_required
def payment_failed(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )

    payment = Payment.objects.filter(
        order=order
    ).first()

    return render(
        request,
        "payments/failed.html",
        {
            "order": order,
            "payment": payment,
        }
    )

def subscribe_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, "Thank you for subscribing!")
            else:
                messages.info(request, "You are already subscribed.")
        return redirect('home')  # Make sure 'home' matches your homepage URL pattern name
    return redirect('home')