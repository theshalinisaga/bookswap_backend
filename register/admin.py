
from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "buyer",
        "total_amount",
        "status",
        "payment_status",
        "estimated_delivery",
    )

    list_filter = (
        "status",
        "payment_status",
        "estimated_delivery",
    )

    search_fields = (
        "buyer__username",
        "full_name",
        "phone",
        "tracking_number",
    )

    readonly_fields = (
        "buyer",
        "subtotal",
        "shipping_fee",
        "total_amount",
        "payment_reference",
        "created_at",
        "updated_at",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "book_title",
        "unit_price",
        "quantity",
    )

    search_fields = ("book_title",)
