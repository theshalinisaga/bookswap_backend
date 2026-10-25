
from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "book",
            "book_title",
            "unit_price",
            "quantity",
        ]
        read_only_fields = [
            "id",
            "book_title",
            "unit_price",
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "buyer",
            "full_name",
            "phone",
            "address_line",
            "city",
            "state",
            "pincode",
            "items",
            "subtotal",
            "shipping_fee",
            "total_amount",
            "status",
            "payment_status",
            "payment_reference",
            "tracking_number",
            "estimated_delivery",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
