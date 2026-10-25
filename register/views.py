from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth.models import User
from register.serializers import (UserSerializer,BookSerializer)
from register.models import Book
class Emp(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
class EmpData(generics.RetrieveAPIView,generics.DestroyAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
class EmpData1(generics.RetrieveUpdateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
class BookListCreate(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Book.objects.all().order_by("-created_at")
    serializer_class = BookSerializer
class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Book.objects.all()
    serializer_class = BookSerializer