"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from register import views as register_views
from login import views as login_views
from django.conf import settings
from django.conf.urls.static import static
from register.order_views import (
    OrderListCreateView,
    OrderDetailView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("emp/",register_views.Emp.as_view(),name="employee"),
    path("emp/<int:pk>/",register_views.EmpData.as_view(),name="empdata"),
    path("emp/<int:pk>/update/",register_views.EmpData1.as_view(),name="empdata1"),
    path("login/", login_views.LoginView.as_view(), name="login"),
    path("books/",register_views.BookListCreate.as_view(),name="books"),
    path("books/<int:pk>/",register_views.BookDetail.as_view(),name="book-detail"),
   path("api/orders/", OrderListCreateView.as_view(), name="orders"),
path("api/orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
