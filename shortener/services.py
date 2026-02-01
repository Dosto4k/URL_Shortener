from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

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


def get_url_title(url: str) -> str:
    """Возвращает title для переданного url"""
    netloc = urlparse(url).netloc
    try:
        response = requests.get(url=url, timeout=1)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return netloc
    if 400 <= response.status_code < 600:
        return netloc
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title
    if title is None:
        return netloc
    return title.text
