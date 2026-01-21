class URLCodeIsAlreadyExistsError(Exception):
    """Вызывается, когда сгенерированный url code уже существует"""


class RetryLimitReachedError(Exception):
    """
    Вызывается, когда был достигнут лимит повторных попыток
    выполнить функцию, обёрнутую декоратором 'retry'
    """


class GenerateURLCodeError(Exception):
    """Вызывается, когда не удалось сгенерировать url code"""
