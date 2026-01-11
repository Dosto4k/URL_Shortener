from rest_framework import serializers

from shortener.models import ShortUrl
from shortener.utils import validate_url_code


class ShortUrlSerializer(serializers.Serializer):
    url = serializers.URLField()
    code = serializers.CharField(
        default=None,
        allow_null=True,
        allow_blank=True,
    )

    def validate_code(self, value: None | str) -> None | str:
        if not value:
            return None
        if not validate_url_code(value):
            raise serializers.ValidationError(
                "Можно использовать только строчные и заглавные "
                "английские буквы, символы '-_' и цифры."
            )
        if ShortUrl.objects.filter(code=value).exists():
            raise serializers.ValidationError(
                "Указанное короткое название URL уже занято."
            )
        return value
