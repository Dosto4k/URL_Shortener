from django.contrib import admin

from shortener.models import ShortURL


@admin.register(ShortURL)
class ShortUrlAdmin(admin.ModelAdmin):
    list_display = ["url", "code", "owner"]
    list_select_related = ["owner"]
