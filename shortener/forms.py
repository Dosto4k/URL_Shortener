from django import forms

from shortener.validators import custom_code_contains_only_allowed_chars, is_unique_code


class CreateShortUrlForm(forms.Form):
    url = forms.URLField()
    custom_code = forms.CharField(label="Пользовательское имя", required=False)

    def clean_custom_code(self) -> str:
        code = self.cleaned_data["custom_code"]
        if code == "":
            return ""
        if not custom_code_contains_only_allowed_chars(code):
            raise forms.ValidationError(
                "В пользовательском имени разрешены строчные и заглавные "
                "буквы английского алфавита, символы «-» и «_» и цифры."
            )
        if not is_unique_code(code):
            raise forms.ValidationError("Указанное пользовательское имя уже занято.")
        return code
