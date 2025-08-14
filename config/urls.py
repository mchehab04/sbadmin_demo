from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("quotes/", include("quotes.urls", namespace="quotes")),
    path("", include("dashboard.urls")),  # your dashboard home
]
