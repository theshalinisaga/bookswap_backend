
import os
import uuid

from django.contrib.auth.models import User
from rest_framework import serializers
from supabase import create_client

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
    image = serializers.ImageField(required=False, write_only=True)
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

    def upload_image(self, image_file):
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

        if not supabase_url or not supabase_key:
            raise serializers.ValidationError(
                "Supabase Storage environment variables are missing."
            )

        client = create_client(supabase_url, supabase_key)

        extension = image_file.name.rsplit(".", 1)[-1].lower()
        file_path = f"books/{uuid.uuid4()}.{extension}"

        image_file.seek(0)
        client.storage.from_("book-images").upload(
            file_path,
            image_file.read(),
            {
                "content-type": image_file.content_type,
                "upsert": "false",
            },
        )

        return client.storage.from_("book-images").get_public_url(file_path)

    def create(self, validated_data):
        image_file = validated_data.pop("image", None)

        # These fields are not database model fields.
        validated_data.pop("seller_name", None)
        validated_data.pop("seller_phone", None)

        if image_file:
            validated_data["image"] = self.upload_image(image_file)

        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        image_file = validated_data.pop("image", None)

        validated_data.pop("seller_name", None)
        validated_data.pop("seller_phone", None)

        if image_file:
            instance.image = self.upload_image(image_file)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["image"] = instance.image or None
        return data