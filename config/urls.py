from debug_toolbar.toolbar import debug_toolbar_urls

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    path("", include("shortener.urls", namespace="shortener")),
] + debug_toolbar_urls()
