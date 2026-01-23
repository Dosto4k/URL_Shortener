from typing import Any

from django import forms

from shortener.exceptions import RetryLimitReachedError
from shortener.models import ShortURL
from shortener.services import generate_unique_code


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
        return super().clean()

    class Meta:
        model = ShortURL
        fields = ["url", "code"]
