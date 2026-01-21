from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from shortener.models import ShortURL


@admin.register(ShortURL)
class ShortUrlAdmin(admin.ModelAdmin):
    list_display = ["url", "code", "is_custom", "url_owner"]

    @admin.display(description="Владелец пользовательской ссылки")
    def url_owner(self, instance: ShortURL) -> str | None:
        """
        Добавляет поле с владельцем короткой ссылки,
        если она создана с пользовательским url code
        """
        if instance.is_custom:
            return instance.users.all()[0].username
        return None

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).prefetch_related("users")
