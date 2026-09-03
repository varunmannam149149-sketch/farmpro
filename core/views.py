from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Subscriber

from .models import User, Product, Order
from .forms import (
    CustomUserCreationForm,
    ProductForm,
    ProfileForm,
    OrderForm
)
from django.db.models import Sum, Count

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Order, Product

from django.shortcuts import render


from payments.models import Payment

from django.contrib import messages
from .models import ContactMessage

from django.core.mail import send_mail
from django.conf import settings


def home(request):
    
    producer_count = User.objects.filter(
        user_type="producer"
    ).count()

    consumer_count = User.objects.filter(
        user_type="consumer"
    ).count()

    market_count = User.objects.filter(
        user_type="market"
    ).count()

    product_count = Product.objects.count()

    context = {
        "producer_count": producer_count,
        "consumer_count": consumer_count,
        "market_count": market_count,
        "product_count": product_count,
    }
    products = Product.objects.filter(
        quantity__gt=0
    ).order_by("-id")[:8]

    
    return render(request, "core/home.html", context)




# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.method == "POST":

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("home")

    else:

        form = CustomUserCreationForm()

    return render(
        request,
        "core/register.html",
        {"form": form}
    )

# =========================================================
# LOGIN
# =========================================================

def user_login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:

            login(request, user)

            # Producer
            if user.user_type == "producer":
                return redirect("producer_dashboard")

            # Consumer
            elif user.user_type == "consumer":
                return redirect("consumer_dashboard")

            # Market
            elif user.user_type == "market":
                return redirect("market_dashboard")

        else:

            messages.error(
                request,
                "Invalid email or password. Please try again."
            )

    return render(
        request,
        "core/login.html"
    )


# =========================================================
# PRODUCER DASHBOARD
# =========================================================

# =========================================================
# PRODUCER DASHBOARD
# =========================================================

@login_required
def producer_dashboard(request):

    if request.user.user_type != "producer":

        messages.error(
            request,
            "You are not authorized to access the Producer Dashboard."
        )

        if request.user.user_type == "consumer":
            return redirect("consumer_dashboard")

        elif request.user.user_type == "market":
            return redirect("market_dashboard")

    # -----------------------------------------------------
    # PRODUCER PRODUCTS
    # -----------------------------------------------------

    products = Product.objects.filter(
        producer=request.user
    )

    # Active/available products
    available_products = products.filter(
        quantity__gt=0
    ).count()

    # Total products
    total_products = products.count()

    # Total quantity
    total_quantity = products.aggregate(
        total=Sum("quantity")
    )["total"] or 0

    # Total inventory value
    inventory_value = 0

    for product in products:
        inventory_value += product.price * product.quantity

    total_inventory_value = inventory_value

    # -----------------------------------------------------
    # PRODUCER ORDERS
    # -----------------------------------------------------

    orders = Order.objects.filter(
        product__producer=request.user
    )

    my_orders = orders.count()

    # -----------------------------------------------------
    # SALES
    # -----------------------------------------------------

    total_sales = orders.filter(
        status__in=["confirmed", "completed"]
    ).aggregate(
        total=Sum("total_price")
    )["total"] or 0

    # -----------------------------------------------------
    # ORDER STATISTICS
    # -----------------------------------------------------

    pending_orders = orders.filter(
        status="pending"
    ).count()

    confirmed_orders = orders.filter(
        status="confirmed"
    ).count()

    completed_orders = orders.filter(
        status="completed"
    ).count()

    cancelled_orders = orders.filter(
        status="cancelled"
    ).count()

    # -----------------------------------------------------
    # RECENT ORDERS
    # -----------------------------------------------------

    recent_orders = orders.select_related(
        "customer",
        "product"
    ).order_by("-created_at")[:5]

    return render(
        request,
        "core/producer_dashboard.html",
        {
            "available_products": available_products,
            "my_orders": my_orders,
            "total_sales": total_sales,

            "total_products": total_products,
            "total_quantity": total_quantity,
            "total_inventory_value": total_inventory_value,

            "pending_orders": pending_orders,
            "confirmed_orders": confirmed_orders,
            "completed_orders": completed_orders,
            "cancelled_orders": cancelled_orders,

            "recent_orders": recent_orders,
        }
    )



# =========================================================
# CONSUMER DASHBOARD
# =========================================================
@login_required
def consumer_dashboard(request):

    if request.user.user_type != "consumer":

        messages.error(
            request,
            "You are not authorized to access the Consumer Dashboard."
        )

        if request.user.user_type == "producer":
            return redirect("producer_dashboard")

        elif request.user.user_type == "market":
            return redirect("market_dashboard")

        return redirect("home")

    available_products = Product.objects.filter(
        quantity__gt=0
    ).count()

    orders = Order.objects.filter(
        customer=request.user
    )

    my_orders = orders.count()

    total_purchase = orders.filter(
        status__in=["confirmed", "completed"]
    ).aggregate(
        total=Sum("total_price")
    )["total"] or 0

    pending_orders = orders.filter(
        status="pending"
    ).count()

    confirmed_orders = orders.filter(
        status="confirmed"
    ).count()

    completed_orders = orders.filter(
        status="completed"
    ).count()

    cancelled_orders = orders.filter(
        status="cancelled"
    ).count()

    recent_orders = Order.objects.filter(customer=request.user).order_by('-created_at')[:5]

    return render(
        request,
        "core/consumer_dashboard.html",
        {
            "available_products": available_products,
            "my_orders": my_orders,
            "total_purchase": total_purchase,

            "pending_orders": pending_orders,
            "confirmed_orders": confirmed_orders,
            "completed_orders": completed_orders,
            "cancelled_orders": cancelled_orders,
            'recent_orders': recent_orders
        }
    )



# =========================================================
# MARKET DASHBOARD
# =========================================================

@login_required
def market_dashboard(request):

    if request.user.user_type != "market":

        messages.error(
            request,
            "You are not authorized to access the Market Dashboard."
        )

        if request.user.user_type == "producer":
            return redirect("producer_dashboard")

        return redirect("consumer_dashboard")

    # -----------------------------------------------------
    # AVAILABLE PRODUCTS
    # -----------------------------------------------------

    available_products = Product.objects.filter(
        quantity__gt=0
    ).count()

    # -----------------------------------------------------
    # PRODUCERS
    # -----------------------------------------------------

    producers = User.objects.filter(
        user_type="producer",
        is_active=True
    ).count()

    # -----------------------------------------------------
    # MARKET ORDERS
    # -----------------------------------------------------

    orders = Order.objects.filter(
        customer=request.user
    )

    market_orders = orders.count()

    # -----------------------------------------------------
    # ORDER STATISTICS
    # -----------------------------------------------------

    pending_orders = orders.filter(
        status="pending"
    ).count()

    confirmed_orders = orders.filter(
        status="confirmed"
    ).count()

    completed_orders = orders.filter(
        status="completed"
    ).count()

    cancelled_orders = orders.filter(
        status="cancelled"
    ).count()



    recent_orders = Order.objects.filter(customer=request.user).order_by('-created_at')[:5]

    
    return render(
        request,
        "core/market_dashboard.html",
        {
            "available_products": available_products,
            "producers": producers,
            "market_orders": market_orders,

            "pending_orders": pending_orders,
            "confirmed_orders": confirmed_orders,
            "completed_orders": completed_orders,
            "cancelled_orders": cancelled_orders,
            'recent_orders': recent_orders
        }
    )



@login_required
def cancel_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        product__producer=request.user
    )

    if request.method == "POST":

        order.status = "cancelled"
        order.cancelled_by = "producer"

        order.cancellation_reason = request.POST.get(
            "cancellation_reason",
            ""
        )

        # Restore stock
        order.product.quantity += order.quantity
        order.product.save()

        order.save()

        messages.success(
            request,
            "Order cancelled successfully."
        )

        return redirect("producer_orders")

    return redirect("producer_orders")



# =========================================================
# ADD PRODUCT
# =========================================================

# =========================================================
# ADD PRODUCT
# =========================================================

@login_required
def add_product(request):

    # Only producers can add products
    if request.user.user_type != "producer":

        messages.error(
            request,
            "Only Producers can add products."
        )

        return redirect("home")

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            product = form.save(
                commit=False
            )

            # Automatically assign logged-in producer
            product.producer = request.user

            # Save product including image
            product.save()

            messages.success(
                request,
                "Product added successfully!"
            )

            return redirect(
                "producer_products"
            )

    else:

        form = ProductForm()

    return render(
        request,
        "core/add_product.html",
        {
            "form": form
        }
    )
# =========================================================
# PRODUCER PRODUCTS
# =========================================================

@login_required
def producer_products(request):

    # Only Producers can access their products
    if request.user.user_type != "producer":

        messages.error(
            request,
            "Only Producers can access their products."
        )

        if request.user.user_type == "consumer":
            return redirect("consumer_dashboard")

        elif request.user.user_type == "market":
            return redirect("market_dashboard")

    # Get only products belonging to logged-in Producer
    products = Product.objects.filter(
        producer=request.user
    ).order_by("-created_at")

    return render(
        request,
        "core/producer_products.html",
        {
            "products": products
        }
    )


# =========================================================
# EDIT PRODUCT
# =========================================================

@login_required
def edit_product(request, product_id):

    # Get only the product belonging to the logged-in producer
    try:
        product = Product.objects.get(
            id=product_id,
            producer=request.user
        )
    except Product.DoesNotExist:
        messages.error(
            request,
            "Product not found or you are not authorized to edit it."
        )
        return redirect("producer_products")

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            instance=product
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Product updated successfully!"
            )

            return redirect("producer_products")

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        "core/edit_product.html",
        {
            "form": form,
            "product": product
        }
    )

# =========================================================
# DELETE PRODUCT
# =========================================================

@login_required
def delete_product(request, product_id):

    # Get only the product belonging to the logged-in producer
    try:
        product = Product.objects.get(
            id=product_id,
            producer=request.user
        )
    except Product.DoesNotExist:
        messages.error(
            request,
            "Product not found or you are not authorized to delete it."
        )
        return redirect("producer_products")

    if request.method == "POST":

        product.delete()

        messages.success(
            request,
            "Product deleted successfully!"
        )

        return redirect("producer_products")

    return render(
        request,
        "core/delete_product.html",
        {
            "product": product
        }
    )

# =========================================================
# BROWSE PRODUCTS MARKET PLACE 
# =========================================================

# =========================================================
# CONSUMER MARKETPLACE
# =========================================================
# =========================================================
# BROWSE PRODUCTS
# =========================================================

@login_required
def browse_products(request):

    products = Product.objects.filter(
        quantity__gt=0
    ).select_related(
        "producer"
    ).order_by(
        "-created_at"
    )

    # Search
    search_query = request.GET.get(
        "search",
        ""
    ).strip()

    if search_query:

        products = products.filter(
            Q(name__icontains=search_query)
            |
            Q(category__icontains=search_query)
            |
            Q(location__icontains=search_query)
        )

    # Categories
    categories = Product.objects.values_list(
        "category",
        flat=True
    ).distinct().order_by(
        "category"
    )

    # Category filter
    selected_category = request.GET.get(
        "category",
        ""
    ).strip()

    if selected_category:

        products = products.filter(
            category=selected_category
        )

    # Location filter
    selected_location = request.GET.get(
        "location",
        ""
    ).strip()

    if selected_location:

        products = products.filter(
            location__icontains=selected_location
        )

    return render(
        request,
        "core/browse_products.html",
        {
            "products": products,
            "categories": categories,
            "search_query": search_query,
            "selected_category": selected_category,
            "selected_location": selected_location,
        }
    )
# =========================================================
# PROFILE
# =========================================================

@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your profile has been updated successfully!"
            )
            return redirect("profile")
    else:
        form = ProfileForm(
            instance=request.user
        )

    # Filtering logic based on user_type
    if request.user.user_type == "producer":
        # Producers see only the products they listed
        products = Product.objects.filter(producer=request.user)
    else:
        # Consumers, Markets, or other roles see all listed products
        products = Product.objects.all()

    return render(
        request,
        "core/profile.html",
        {
            "form": form,
            "products": products,
        }
    )
# =========================================================
# PLACE ORDER
# =========================================================

@login_required
def place_order(request, product_id):

    # Only Consumers can place orders
    # Only Consumers and Markets can place orders
    if request.user.user_type not in ["consumer", "market"]:

        messages.error(
        request,
        "Only Consumers and Markets can place orders."
    )

        return redirect("producer_dashboard")

    # Get the selected product
    try:

        product = Product.objects.get(
            id=product_id
        )

    except Product.DoesNotExist:

        messages.error(
            request,
            "Product not found."
        )

        return redirect("browse_products")

    if request.method == "POST":

        form = OrderForm(request.POST)

        if form.is_valid():

            quantity = form.cleaned_data["quantity"]

            # Check available quantity
            if quantity > product.quantity:

                form.add_error(
                    "quantity",
                    "Requested quantity is not available."
                )

            else:

                # Calculate total price
                total_price = (
                    quantity * product.price
                )

                # Create order
                order = form.save(commit=False)

                order.customer = request.user
                order.product = product
                order.total_price = total_price

                order.save()

                # Reduce product stock
                product.quantity -= quantity
                product.save()

                messages.success(
            request,
            "Your order has been placed successfully!"
        )

        if request.user.user_type == "market":
            return redirect("market_orders")

        return redirect("my_orders")
    else:

        form = OrderForm()

    return render(
        request,
        "core/place_order.html",
        {
            "form": form,
            "product": product
        }
    )

# =========================================================
# MY ORDERS - CONSUMER
# =========================================================

# =========================================================
# MY ORDERS - CONSUMER / MARKET
# =========================================================

@login_required
def my_orders(request):

    from payments.models import Payment

    orders = Order.objects.filter(
        customer=request.user
    ).select_related(
        "product"
    ).order_by(
        "-created_at"
    )

    # -----------------------------------------------------
    # Attach payment safely to each order
    # -----------------------------------------------------
    for order in orders:

        order.farmpro_payment = Payment.objects.filter(
            order=order
        ).first()

    return render(
        request,
        "core/my_orders.html",
        {
            "orders": orders
        }
    )
# =========================================================
# CONSUMER ORDERS CANCEL
# =========================================================

# =========================================================
# CONSUMER CANCEL ORDER
# =========================================================

@login_required
def consumer_cancel_order(request, order_id):

    if request.user.user_type not in ["consumer", "market"]:

        messages.error(
            request,
            "Only Consumers and Markets can cancel their orders."
        )

        return redirect("consumer_dashboard")


    # Get only this user's order
    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )


    # Only pending or confirmed orders can be cancelled
    if order.status not in ["pending", "confirmed"]:

        messages.error(
            request,
            "This order can no longer be cancelled."
        )

        if request.user.user_type == "market":
            return redirect("market_orders")

        return redirect("my_orders")


    if request.method == "POST":

        reason = request.POST.get(
            "cancellation_reason",
            ""
        ).strip()


        # -------------------------------------------------
        # RESTORE PRODUCT STOCK
        # -------------------------------------------------

        product = order.product

        product.quantity += order.quantity

        product.save()


        # -------------------------------------------------
        # UPDATE ORDER
        # -------------------------------------------------

        order.status = "cancelled"

        order.cancelled_by = "consumer"

        order.cancellation_reason = reason

        order.save()


        messages.success(
            request,
            f"Order #{order.id} cancelled successfully. "
            f"The product stock has been restored."
        )


        # Redirect based on user type
        if request.user.user_type == "market":
            return redirect("market_orders")

        return redirect("my_orders")


    return render(
        request,
        "core/cancel_order.html",
        {
            "order": order,
            "user_type": request.user.user_type
        }
    )

# =========================================================
# PRODUCER ORDERS
# =========================================================
@login_required
def producer_orders(request):

    orders = Order.objects.filter(
        product__producer=request.user
    ).select_related(
        "product",
        "customer"
    ).order_by(
        "-created_at"
    )

    pending_orders = orders.filter(
        status="pending"
    ).count()

    confirmed_orders = orders.filter(
        status="confirmed"
    ).count()

    completed_orders = orders.filter(
        status="completed"
    ).count()

    cancelled_orders = orders.filter(
        status="cancelled"
    ).count()

    context = {
        "orders": orders,
        "pending_orders": pending_orders,
        "confirmed_orders": confirmed_orders,
        "completed_orders": completed_orders,
        "cancelled_orders": cancelled_orders,
    }

    return render(
        request,
        "core/producer_orders.html",
        context
    )

# =========================================================
# CONFIRM  ORDERS
# =========================================================

# =========================================================
# CONFIRM ORDER
# =========================================================

# =========================================================
# CONFIRM ORDER
# =========================================================

@login_required
def confirm_order(request, order_id):

    from payments.models import Payment

    # -------------------------------------------------
    # Find the order belonging to this producer
    # -------------------------------------------------

    order = get_object_or_404(
        Order,
        id=order_id,
        product__producer=request.user
    )

    # -------------------------------------------------
    # Only pending orders can be confirmed
    # -------------------------------------------------

    if order.status != "pending":

        return redirect("producer_orders")

    # -------------------------------------------------
    # Confirm the order
    # -------------------------------------------------

    order.status = "confirmed"

    order.save(
        update_fields=["status"]
    )

    # -------------------------------------------------
    # Create payment record
    # -------------------------------------------------

    Payment.objects.get_or_create(

        order=order,

        defaults={
            "amount": order.total_price,
            "producer_upi_id": request.user.upi_id,
            "status": "pending",
        }
    )

    # -------------------------------------------------
    # Return to Producer Orders
    # -------------------------------------------------

    return redirect("producer_orders")


@login_required
def producer_payment_received(request, order_id):

    from payments.models import Payment
    from django.utils import timezone

    # -------------------------------------------------
    # Find order belonging to this producer
    # -------------------------------------------------

    order = get_object_or_404(
        Order,
        id=order_id,
        product__producer=request.user
    )

    # -------------------------------------------------
    # Only confirmed orders can be marked as paid
    # -------------------------------------------------

    if order.status != "confirmed":

        return redirect("producer_orders")

    # -------------------------------------------------
    # Get payment
    # -------------------------------------------------

    payment = get_object_or_404(
        Payment,
        order=order
    )

    # -------------------------------------------------
    # Mark payment as received
    # -------------------------------------------------

    payment.status = "paid"

    payment.paid_at = timezone.now()

    payment.save(
        update_fields=[
            "status",
            "paid_at"
        ]
    )

    # -------------------------------------------------
    # Complete the order
    # -------------------------------------------------

    order.status = "completed"

    order.save(
        update_fields=["status"]
    )

    # -------------------------------------------------
    # Return to Producer Orders
    # -------------------------------------------------

    return redirect("producer_orders")


# =========================================================
# CANCEL ORDERS
# =========================================================
# =========================================================
# PRODUCER CANCEL ORDER
# =========================================================

@login_required
def producer_cancel_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        product__producer=request.user
    )

    # -------------------------------------------------
    # GET → SHOW CANCELLATION FORM
    # -------------------------------------------------

    if request.method == "GET":

        return render(
            request,
            "core/cancel_order.html",
            {
                "order": order,
                "user_type": "producer",
            }
        )

    # -------------------------------------------------
    # POST → PROCESS CANCELLATION
    # -------------------------------------------------

    if request.method == "POST":

        reason = request.POST.get("cancellation_reason", "").strip()

        other_reason = request.POST.get(
            "other_reason",
            ""
        ).strip()

        # ---------------------------------------------
        # VALIDATION
        # ---------------------------------------------

        if not reason:

            messages.error(
                request,
                "Please select a cancellation reason."
            )

            return redirect(
                "producer_cancel_order",
                order_id=order.id
            )

        # ---------------------------------------------
        # OTHER
        # ---------------------------------------------

        if reason == "other":

            if not other_reason:

                messages.error(
                    request,
                    "Please enter your reason."
                )

                return redirect(
                    "producer_cancel_order",
                    order_id=order.id
                )

            final_reason = other_reason

        else:

            reason_names = {
                "product_unavailable":
                    "Product unavailable",

                "quantity_unavailable":
                    "Required quantity unavailable",

                "price_issue":
                    "Price issue",

                "delivery_issue":
                    "Delivery / transportation issue",

                "buyer_request":
                    "Buyer requested cancellation",
            }

            final_reason = reason_names.get(
                reason,
                "Other"
            )

        # ---------------------------------------------
        # CHECK ORDER STATUS
        # ---------------------------------------------

        if order.status not in [
            "pending",
            "confirmed"
        ]:

            messages.error(
                request,
                "This order cannot be cancelled."
            )

            return redirect("producer_orders")

        # ---------------------------------------------
        # RESTORE STOCK
        # ---------------------------------------------

        order.product.quantity += order.quantity
        order.product.save()

        # ---------------------------------------------
        # UPDATE ORDER
        # ---------------------------------------------

        order.status = "cancelled"

        order.cancelled_by = "producer"

        order.cancellation_reason = final_reason

        order.save()

        messages.success(
            request,
            f"Order #{order.id} cancelled successfully."
        )

        return redirect("producer_orders")

    
# =========================================================
# COMPLETE ORDERS
# =========================================================
# =========================================================
# COMPLETE ORDER
# =========================================================

# =========================================================
# COMPLETE ORDER
# =========================================================

@login_required
def complete_order(request, order_id):

    if request.method != "POST":

        messages.error(
            request,
            "Invalid request."
        )

        return redirect("producer_orders")


    order = get_object_or_404(
        Order,
        id=order_id,
        product__producer=request.user
    )


    if order.status != "confirmed":

        messages.error(
            request,
            "Only confirmed orders can be completed."
        )

        return redirect("producer_orders")


    order.status = "completed"

    order.save()


    messages.success(
        request,
        f"Order #{order.id} marked as completed."
    )


    return redirect("producer_orders")


# =========================================================
# MARKET ORDERS
# =========================================================

@login_required
def market_orders(request):

    # Only Markets can access orders
    if request.user.user_type != "market":

        messages.error(
            request,
            "Only Markets can access market orders."
        )

        if request.user.user_type == "producer":
            return redirect("producer_dashboard")

        elif request.user.user_type == "consumer":
            return redirect("consumer_dashboard")

    orders = Order.objects.filter(
        customer=request.user
    ).select_related(
        "product",
        "product__producer"
    ).order_by("-created_at")

    return render(
        request,
        "core/market_orders.html",
        {
            "orders": orders
        }
    )


# =========================================================
# MARKET ACCEPT ORDER
# =========================================================

@login_required
def market_accept_order(request, order_id):

    if request.user.user_type != "market":

        messages.error(
            request,
            "Only Markets can accept orders."
        )

        if request.user.user_type == "producer":
            return redirect("producer_dashboard")

        elif request.user.user_type == "consumer":
            return redirect("consumer_dashboard")

    try:

        order = Order.objects.get(
            id=order_id,
            customer=request.user
        )

    except Order.DoesNotExist:

        messages.error(
            request,
            "Order not found."
        )

        return redirect("market_orders")

    if order.status == "pending":

        order.status = "confirmed"
        order.save()

        messages.success(
            request,
            "Order accepted successfully!"
        )

    else:

        messages.warning(
            request,
            "This order cannot be accepted."
        )

    return redirect("market_orders")




# About Page
def about(request):
    return render(request, "core/about.html")


# Contact Page
def contact(request):
    return render(request, "core/contact.html")



def subscribe_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, "Thank you for subscribing!")
            else:
                messages.info(request, "You are already subscribed.")
    return redirect('home')


from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage

def contact_view(request):
    print(f"\n--- REQUEST METHOD: {request.method} ---")
    
    if request.method == 'POST':
        print("--- INSIDE POST BLOCK ---")
        name = request.POST.get('name')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        print(f"Form Data: Name={name}, Email={email}, Subject={subject}")

        # Save to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            user_type=user_type,
            subject=subject,
            message=message
        )
        print("Database record created!")

        # Send email with explicit try/except error trapping
        try:
            print("Attempting send_mail()...")
            sent_count = send_mail(
                subject=f"FARMPRO Contact: {subject}",
                message=f"From: {name} ({email})\nUser Type: {user_type}\n\nMessage:\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            print(f"SUCCESS! Email count sent: {sent_count}")
            messages.success(request, "Your message has been sent successfully!")
        except Exception as err:
            print(f"EMAIL FAILED ERROR: {err}")
            messages.error(request, f"Message saved to database, but email failed: {err}")

        return redirect('contact')

    return render(request, 'core/contact.html')


# =========================================================
# LOGOUT
# =========================================================

def user_logout(request):

    logout(request)

    return redirect("login")


# def user_logout(request):
#     logout(request)
#     return redirect("/register/?mode=login")