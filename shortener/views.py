from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, FormView, View, RedirectView

from shortener.exceptions import GenerateURLCodeError
from shortener.forms import CreateShortUrlForm
from shortener.models import ShortURL
from shortener.services import (
    create_short_url_with_custom_code,
    create_short_url_with_generate_code,
    check_short_url_owner,
)


class HomePage(TemplateView):
    template_name = "shortener/home.html"


class CreateShortURL(LoginRequiredMixin, FormView):
    template_name = "shortener/create_short_url.html"
    form_class = CreateShortUrlForm

    def form_valid(self, form: CreateShortUrlForm) -> HttpResponse:
        form_data = form.cleaned_data
        custom_code = form_data.get("custom_code")
        if custom_code is None or custom_code == "":
            try:
                short_url = create_short_url_with_generate_code(
                    form_data,
                    self.request.user,  # type: ignore
                )
            except GenerateURLCodeError:
                form.add_error(
                    field=None,
                    error="Не удалось создать короткий URL. Попробуйте ещё раз.",
                )
                return super().form_invalid(form)
        else:
            short_url = create_short_url_with_custom_code(form_data, self.request.user)  # type: ignore
        self.kwargs["code"] = short_url.code
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(
            "shortener:create-short-url-done", kwargs={"code": self.kwargs.get("code")}
        )


class CreateShortURLDone(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:  # noqa:ANN003,
        short_url = get_object_or_404(ShortURL, code=kwargs.get("code"))
        if not check_short_url_owner(short_url, request.user):  # type:ignore
            raise Http404
        context = {
            "short_url": short_url,
        }
        return render(request, "shortener/create_short_url_done.html", context)


class RedirectByShortUrl(RedirectView):
    permanent = True

    def get_redirect_url(self, **kwargs) -> str:  # noqa:ANN003
        short_url = get_object_or_404(ShortURL, code=kwargs.get("code"))
        return short_url.url
