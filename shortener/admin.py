from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest

from shortener.models import ShortURL
from shortener.services import generate_unique_code, get_url_title


@admin.register(ShortURL)
class ShortUrlAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "url", "code", "owner"]
    list_select_related = ["owner"]

    def save_model(
        self, request: HttpRequest, obj: ShortURL, form: ModelForm, change: bool
    ) -> None:
        """Генерирует url code, если он отсутствует"""
        if obj.code is None or obj.code == "":
            obj.code = generate_unique_code()
        if obj.title is None or obj.title == "":
            obj.title = get_url_title(obj.url)
        return super().save_model(request, obj, form, change)
