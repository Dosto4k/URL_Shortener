from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.http import Http404
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    RedirectView,
    TemplateView,
    View,
)

from shortener.forms import CreateShortUrlForm
from shortener.models import ShortURL


class HomePage(TemplateView):
    template_name = "shortener/home.html"


class CreateShortURL(LoginRequiredMixin, CreateView):
    template_name = "shortener/create_short_url.html"
    form_class = CreateShortUrlForm

    def form_valid(self, form: CreateShortUrlForm) -> HttpResponse:
        filters = {
            "url": form.cleaned_data["url"],
            "owner": self.request.user,
        }
        if ShortURL.get_object_or_none(**filters) is not None:
            form.add_error(
                field="url", error="У вас уже есть короткий URL для указанного URL."
            )
            return super().form_invalid(form)
        short_url = form.save(commit=False)
        short_url.owner = self.request.user
        self.kwargs["code"] = short_url.code
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(
            "shortener:create-short-url-done", kwargs={"code": self.kwargs.get("code")}
        )


class CreateShortURLDone(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:  # noqa:ANN003
        short_url = get_object_or_404(ShortURL, code=kwargs.get("code"))
        if not short_url.owner == request.user:
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


class ListShortURL(LoginRequiredMixin, ListView):
    template_name = "shortener/list_short_url.html"
    paginator_class = Paginator
    paginate_by = 4

    def get_queryset(self) -> QuerySet[Any]:
        return ShortURL.objects.filter(owner=self.request.user)


class DetailShortURL(LoginRequiredMixin, DetailView):
    template_name = "shortener/detail_short_url.html"

    def get_queryset(self) -> QuerySet[ShortURL]:
        return ShortURL.objects.filter(owner=self.request.user)
