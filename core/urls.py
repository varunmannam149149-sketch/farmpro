from django.urls import path
from . import views


urlpatterns = [

    # =========================================================
    # HOME
    # =========================================================

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "about/",
        views.about,
        name="about"
    ),

    # path(
    #     "contact/",
    #     views.contact,
    #     name="contact"
    # ),


    # =========================================================
    # AUTHENTICATION
    # =========================================================

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "login/",
        views.user_login,
        name="login"
    ),

    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),


    # =========================================================
    # DASHBOARDS
    # =========================================================

    path(
        "producer/dashboard/",
        views.producer_dashboard,
        name="producer_dashboard"
    ),

    path(
        "consumer/dashboard/",
        views.consumer_dashboard,
        name="consumer_dashboard"
    ),

    path(
        "market/dashboard/",
        views.market_dashboard,
        name="market_dashboard"
    ),


    # =========================================================
    # PRODUCTS
    # =========================================================

    path(
        "products/add/",
        views.add_product,
        name="add_product"
    ),

    path(
        "products/",
        views.producer_products,
        name="producer_products"
    ),

    path(
        "products/<int:product_id>/edit/",
        views.edit_product,
        name="edit_product"
    ),

    path(
        "products/<int:product_id>/delete/",
        views.delete_product,
        name="delete_product"
    ),


    # =========================================================
    # MARKETPLACE
    # =========================================================

    path(
        "marketplace/",
        views.browse_products,
        name="browse_products"
    ),

    path(
        "products/<int:product_id>/order/",
        views.place_order,
        name="place_order"
    ),


    # =========================================================
    # PROFILE
    # =========================================================

    path(
        "profile/",
        views.profile,
        name="profile"
    ),


    # =========================================================
    # CUSTOMER / CONSUMER ORDERS
    # =========================================================

    path(
        "orders/",
        views.my_orders,
        name="my_orders"
    ),

    path(
        "orders/<int:order_id>/cancel/",
        views.consumer_cancel_order,
        name="consumer_cancel_order"
    ),


    # =========================================================
    # PRODUCER ORDERS
    # =========================================================

    path(
        "producer/orders/",
        views.producer_orders,
        name="producer_orders"
    ),

    path(
    "producer/orders/<int:order_id>/confirm/",
    views.confirm_order,
    name="confirm_order"
),

path(
    "producer/orders/<int:order_id>/payment-received/",
    views.producer_payment_received,
    name="producer_payment_received"
),

path(
    "producer/orders/<int:order_id>/cancel/",
    views.producer_cancel_order,
    name="producer_cancel_order"
),

    path(
        "producer/orders/<int:order_id>/cancel/",
        views.producer_cancel_order,
        name="producer_cancel_order"
    ),

    path(
        "producer/orders/<int:order_id>/complete/",
        views.complete_order,
        name="complete_order"
    ),


    # =========================================================
    # MARKET ORDERS
    # =========================================================

    path(
        "market/orders/",
        views.market_orders,
        name="market_orders"
    ),

    path(
        "market/orders/<int:order_id>/accept/",
        views.market_accept_order,
        name="market_accept_order"
    ),
    path('subscribe/', views.subscribe_view, name='subscribe'),
    path('contact/', views.contact_view, name='contact'),

]