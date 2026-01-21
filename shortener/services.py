from typing import Any

from django.contrib.auth.models import User
from django.db.transaction import atomic

from shortener.decorators import retry
from shortener.exceptions import (
    URLCodeIsAlreadyExistsError,
    RetryLimitReachedError,
    GenerateURLCodeError,
)
from shortener.models import ShortURL
from shortener.utils import generate_code
from shortener.validators import is_unique_code


@retry(exceptions=(URLCodeIsAlreadyExistsError,))
def generate_unique_code() -> str:
    """Генерирует уникальный url code"""
    code = generate_code()
    if is_unique_code(code):
        return code
    raise URLCodeIsAlreadyExistsError("URL code уже существует.")


def create_short_url_with_custom_code(data: dict[str, Any], user: User) -> ShortURL:
    """
    Создаёт ShortUrl с пользовательским url
    code и связывает его с пользователем user
    """
    with atomic():
        short_url = ShortURL.objects.create(
            url=data["url"], code=data["custom_code"], is_custom=True
        )
        short_url.users.add(user)
    return short_url


def create_short_url_with_generate_code(data: dict[str, Any], user: User) -> ShortURL:
    """
    Создаёт ShortUrl со сгенерированным url code
    и связывает его с пользователем user
    """
    try:
        short_url = ShortURL.objects.get(url=data["url"], is_custom=False)
    except ShortURL.DoesNotExist:
        short_url = None

    if short_url is not None:
        short_url.users.add(user)
        return short_url
    try:
        code = generate_unique_code()
    except RetryLimitReachedError as err:
        raise GenerateURLCodeError("Не удалось сгенерировать url code.") from err
    with atomic():
        short_url = ShortURL.objects.create(url=data["url"], code=code, is_custom=False)
        short_url.users.add(user)
    return short_url


def check_short_url_owner(short_url: ShortURL, user: User) -> bool:
    """Проверяет, владеет ли пользователь user короткой ссылкой short_url"""
    return short_url.users.filter(pk=user.pk).exists()
