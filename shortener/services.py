from django.db.utils import IntegrityError

from shortener.decorators import retry
from shortener.exceptions import LimitRetriesError, GenerateUrlCodeError
from shortener.models import ShortUrl
from shortener.utils import generate_url_code


@retry(exceptions=(IntegrityError,))
def generate_unique_url_code() -> str:
    """Генерирует url code которого ещё не в бд"""
    code = generate_url_code()
    if ShortUrl.objects.filter(code=code).exists():
        raise IntegrityError("UNIQUE constraint failed: shortener_shorturl.code")
    return code


def create_default_short_url(data: dict) -> str:
    """
    Создаёт и связывает url code с ссылкой и возвращает короткую ссылку.
    Если ссылка уже связана с url code и не является пользовательской,
    возвращает существующую короткую ссылку.
    """
    objects = [
        obj for obj in ShortUrl.objects.filter(url=data["url"], custom_code=False)
    ]
    if objects:
        code = objects[0].code
    else:
        try:
            code = generate_unique_url_code()
        except LimitRetriesError as err:
            raise GenerateUrlCodeError("Не удалось сгенерировать url code.") from err
        ShortUrl.objects.create(url=data["url"], code=code, custom_code=False)
    return f"http://127.0.0.1:8000/{code}/"


def create_custom_short_url(data: dict) -> str:
    """
    Связывает пользовательский url code с ссылкой и возвращает короткую ссылку.
    """
    ShortUrl.objects.create(url=data["url"], code=data["code"], custom_code=True)
    return f"http://127.0.0.1:8000/{data['code']}/"


def get_url_by_code(code: str) -> str | None:
    """
    Получает ShortUrl из БД по коду code и возвращает URL для редиректа.
    """
    try:
        short_url = ShortUrl.objects.get(code=code)
    except ShortUrl.DoesNotExist:
        return None
    return short_url.url
