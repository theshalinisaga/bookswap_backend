
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class BookSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    seller_name = serializers.CharField(required=False, allow_blank=True)
    seller_phone = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "price",
            "category",
            "description",
            "image",
            "seller_name",
            "seller_phone",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
