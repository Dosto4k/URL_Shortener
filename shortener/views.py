from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from django.http.response import HttpResponsePermanentRedirect, HttpResponse

from shortener.exceptions import GenerateUrlCodeError
from shortener.serializers import ShortUrlSerializer
from shortener.services import (
    create_default_short_url,
    create_custom_short_url,
    get_url_by_code,
)


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


class RedirectByURLCode(APIView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs) -> HttpResponse:  # noqa ANN003,ARG002,ANN002,ANN001
        code = kwargs.get("code")
        failure_response = Response(
            data={"detail": "Короткий url для переданного url code не существует."},
            status=status.HTTP_400_BAD_REQUEST,
        )
        if code is None:
            return failure_response
        url = get_url_by_code(code)
        if url is None:
            return failure_response
        return HttpResponsePermanentRedirect(url)
