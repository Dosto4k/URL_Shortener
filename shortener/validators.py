from django.conf import settings
from django.core.exceptions import ValidationError


def code_contains_only_allowed_chars(code: str) -> None:
    """Проверяет, состоит ли url code только из допустимых символов"""
    allowed_chars = set(settings.URL_CODE_ALLOWED_CHARS)
    if not all(char in allowed_chars for char in code):
        raise ValidationError(
            "В URL коде разрешены строчные и заглавные "
            "буквы английского алфавита, символы «-» и «_» и цифры."
        )
