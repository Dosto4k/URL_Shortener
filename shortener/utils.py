import random

from django.conf import settings


def generate_code() -> str:
    """Генерирует 8-значный url code из допустимых символов"""
    return "".join(
        random.choices(settings.URL_CODE_ALLOWED_CHARS, k=settings.URL_CODE_LENGTH)  # noqa:S311
    )
