class LimitRetriesError(Exception):
    """
    Вызывается, когда превышено количество повторных попыток.
    """


class GenerateUrlCodeError(Exception):
    """
    Вызывается, когда не удалось сгенерировать url code.
    """
