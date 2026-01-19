from debug_toolbar.toolbar import debug_toolbar_urls

from django.contrib import admin
from django.urls import path, include

# Временный import
from django.views.generic import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    # Временный path
    path("", TemplateView.as_view(template_name="base.html"), name="home"),
] + debug_toolbar_urls()
