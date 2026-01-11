from random import choices
from string import digits, ascii_letters


def generate_url_code() -> str:
    """
    Генерирует случайный url code для короткой ссылки.
    """
    return "".join(choices(digits + ascii_letters + "-_", k=8))  # noqa:S311


def validate_url_code(code: str) -> bool:
    """
    Валидирует пользовательский url code на наличие недопустимых символов
    """
    allowed_chars = set(digits + ascii_letters + "-_")
    return all(char in allowed_chars for char in code)
