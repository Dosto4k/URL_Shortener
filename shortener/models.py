from django.db import models
from django.contrib.auth import get_user_model


class ShortURL(models.Model):
    url = models.CharField(verbose_name="URL")
    code = models.CharField(verbose_name="Код URL", unique=True)
    is_custom = models.BooleanField(verbose_name="Пользовательский ли код")
    users = models.ManyToManyField(
        get_user_model(), related_name="urls", verbose_name="Владельцы"
    )

    def __str__(self) -> str:
        return f"Url: {self.url} Code: {self.code}"

    def __repr__(self) -> str:
        return "{cls_name}(url={url}, code={code}, is_custom={is_custom})".format(
            cls_name=self.__class__.__name__,
            url=self.url,
            code=self.code,
            is_custom=self.is_custom,
        )

    class Meta:
        verbose_name = "Короткая ссылка"
        verbose_name_plural = "Короткие ссылки"
