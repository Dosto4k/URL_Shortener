from typing import Any

from django import forms

from shortener.exceptions import RetryLimitReachedError
from shortener.models import ShortURL
from shortener.services import generate_unique_code, get_url_title


class CreateShortUrlForm(forms.ModelForm):
    def clean(self) -> dict[str, Any]:
        if not self.cleaned_data["code"]:
            try:
                self.cleaned_data["code"] = generate_unique_code()
            except RetryLimitReachedError:
                self.add_error(
                    field="code",
                    error=forms.ValidationError(
                        "Не удалось создать короткий URL. Попробуйте ещё раз."
                    ),
                )
        if not self.cleaned_data["title"]:
            self.cleaned_data["title"] = get_url_title(self.cleaned_data["url"])
        return super().clean()

    class Meta:
        model = ShortURL
        fields = ["url", "title", "code"]
        labels = {
            "title": "Название (Не обязательно)",
            "code": "URL код (Не обязательно)",
        }
