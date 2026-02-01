from typing import Self

from django.db import models
from django.contrib.auth import get_user_model

from shortener.validators import code_contains_only_allowed_chars


class ShortURL(models.Model):
    url = models.URLField(verbose_name="URL")
    code = models.CharField(
        verbose_name="URL код",
        unique=True,
        max_length=50,
        blank=True,
        validators=[code_contains_only_allowed_chars],
        error_messages={"unique": "Указанный URL код уже существует."},
        db_index=True,
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="urls",
        verbose_name="Владелец",
    )

    class Meta:
        verbose_name = "Короткая ссылка"
        verbose_name_plural = "Короткие ссылки"
        constraints = [
            models.UniqueConstraint(
                fields=["url", "owner"],
                name="unique_url_owner",
                violation_error_message=(
                    "У пользователя уже есть короткий URL для указанного URL."
                ),
            )
        ]

    def __str__(self) -> str:
        return f"Url: {self.url} Code: {self.code}"

    def __repr__(self) -> str:
        return "{cls_name}(url={url}, code={code})".format(
            cls_name=self.__class__.__name__,
            url=self.url,
            code=self.code,
        )

    @classmethod
    def get_object_or_none(cls, **filters) -> Self | None:  # noqa:ANN003
        """Возвращает ShortURL по фильтрам или None, если его не существует"""
        try:
            obj = cls.objects.get(**filters)
        except cls.DoesNotExist:
            return None
        return obj
