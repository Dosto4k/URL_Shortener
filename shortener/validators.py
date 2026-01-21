from django.conf import settings

from shortener.models import ShortURL


def custom_code_contains_only_allowed_chars(code: str) -> bool:
    """
    Проверяет, состоит ли введённый пользователем
    url code только из допустимых символов
    """
    allowed_chars = set(settings.URL_CODE_ALLOWED_CHARS)
    return all(char in allowed_chars for char in code)


def is_unique_code(code: str) -> bool:
    """Проверяет уникальность url code"""
    try:
        ShortURL.objects.get(code=code)
    except ShortURL.DoesNotExist:
        return True
    return False
