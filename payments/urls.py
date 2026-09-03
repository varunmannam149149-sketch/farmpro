from django.urls import path

from . import views

from django.urls import path, include

    
app_name = "payments"


urlpatterns = [

    path(
        "checkout/<int:order_id>/",
        views.checkout,
        name="checkout"
    ),

    path(
        "success/<int:order_id>/",
        views.payment_success,
        name="success"
    ),

    path(
        "failed/<int:order_id>/",
        views.payment_failed,
        name="failed"
    ),

    path('subscribe/', views.subscribe_view, name='subscribe'),
]