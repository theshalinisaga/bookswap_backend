
from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP

from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Book, Order, OrderItem
from .order_serializers import OrderSerializer


SHIPPING_FEE = Decimal("50.00")
DELIVERY_DAYS = 5


class OrderListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = (
            Order.objects
            .filter(buyer=request.user)
            .prefetch_related("items")
            .order_by("-created_at")
        )

        return Response(OrderSerializer(orders, many=True).data)

    def post(self, request):
        data = request.data

        required_fields = [
            "full_name",
            "phone",
            "address_line",
            "city",
            "state",
            "pincode",
            "items",
        ]

        for field in required_fields:
            if field not in data or data[field] in ("", None, []):
                return Response(
                    {"error": f"{field} is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if not isinstance(data["items"], list):
            return Response(
                {"error": "Items must be a list."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not data["items"]:
            return Response(
                {"error": "Your cart is empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with transaction.atomic():
                subtotal = Decimal("0.00")
                validated_items = []

                for item in data["items"]:
                    book_id = item.get("book", item.get("book_id"))
                    quantity = item.get("quantity")

                    if not book_id or isinstance(quantity, bool):
                        raise ValueError(
                            "Each item needs a valid book ID and quantity."
                        )

                    try:
                        quantity = int(quantity)
                    except (TypeError, ValueError):
                        raise ValueError("Quantity must be a whole number.")

                    if quantity < 1 or quantity > 100:
                        raise ValueError(
                            "Quantity must be between 1 and 100."
                        )

                    book = get_object_or_404(
                        Book.objects.select_for_update(),
                        pk=book_id,
                    )

                    unit_price = Decimal(str(book.price)).quantize(
                        Decimal("0.01"),
                        rounding=ROUND_HALF_UP,
                    )

                    subtotal += unit_price * quantity
                    validated_items.append(
                        (book, quantity, unit_price)
                    )

                subtotal = subtotal.quantize(Decimal("0.01"))
                shipping_fee = SHIPPING_FEE
                total_amount = subtotal + shipping_fee

                order = Order.objects.create(
                    buyer=request.user,
                    full_name=str(data["full_name"]).strip(),
                    phone=str(data["phone"]).strip(),
                    address_line=str(data["address_line"]).strip(),
                    city=str(data["city"]).strip(),
                    state=str(data["state"]).strip(),
                    pincode=str(data["pincode"]).strip(),
                    subtotal=subtotal,
                    shipping_fee=shipping_fee,
                    total_amount=total_amount,
                    status="pending",
                    payment_status="pending",
                    estimated_delivery=(
                        timezone.localdate()
                        + timedelta(days=DELIVERY_DAYS)
                    ),
                )

                for book, quantity, unit_price in validated_items:
                    OrderItem.objects.create(
                        order=order,
                        book=book,
                        book_title=book.title,
                        unit_price=unit_price,
                        quantity=quantity,
                    )

        except ValueError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "message": (
                    "Order created. Payment is pending; "
                    "this does not mean payment was received."
                ),
                "order": OrderSerializer(order).data,
            },
            status=status.HTTP_201_CREATED,
        )


class OrderDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(
            Order.objects.prefetch_related("items"),
            pk=pk,
            buyer=request.user,
        )

        return Response(OrderSerializer(order).data)
