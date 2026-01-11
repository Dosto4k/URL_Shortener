from functools import wraps

from shortener.exceptions import LimitRetriesError


def retry(exceptions: tuple[type[Exception], ...], max_retries: int = 5):  # noqa ANN201
    """
    Перезапускает функцию max_retries раз при возникновении исключения из exceptions.
    """

    def decorator(func):  # noqa:ANN001,ANN202
        @wraps(func)
        def wrapper(*args, **kwargs):  # noqa:ANN003,ANN002,ANN202
            curr_retries = 0
            while curr_retries < max_retries:
                try:
                    res = func(*args, **kwargs)
                except exceptions:
                    curr_retries += 1
                else:
                    return res
            raise LimitRetriesError("Достигнуто максимальное число повторных попыток.")

        return wrapper

    return decorator
