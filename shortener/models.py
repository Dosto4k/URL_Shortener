from django.db import models


class ShortUrl(models.Model):
    url = models.URLField()
    code = models.CharField(unique=True)
    custom_code = models.BooleanField()
