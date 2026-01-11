from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from shortener.exceptions import GenerateUrlCodeError
from shortener.serializers import ShortUrlSerializer
from shortener.services import create_default_short_url, create_custom_short_url


class CreateShortUrlView(GenericAPIView):
    serializer_class = ShortUrlSerializer
    http_method_names = ["post"]

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not serializer.validated_data["code"]:
            try:
                short_url = create_default_short_url(serializer.validated_data)
            except GenerateUrlCodeError:
                return Response(
                    {"detail": "Не удалось сгенерировать url"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            short_url = create_custom_short_url(serializer.validated_data)
        return Response({"short_url": short_url}, status=status.HTTP_201_CREATED)
