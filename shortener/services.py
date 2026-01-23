from shortener.decorators import retry
from shortener.exceptions import (
    URLCodeIsAlreadyExistsError,
)
from shortener.models import ShortURL
from shortener.utils import generate_code


@retry(exceptions=(URLCodeIsAlreadyExistsError,))
def generate_unique_code() -> str:
    """Генерирует уникальный url code"""
    code = generate_code()
    if ShortURL.get_object_or_none(code=code) is None:
        return code
    raise URLCodeIsAlreadyExistsError("URL code уже существует.")
