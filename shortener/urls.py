from django.urls import path

from shortener import views

app_name = "shortener"
urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path(
        "u/<str:code>/",
        views.RedirectByShortUrl.as_view(),
        name="redirect-by-short-url",
    ),
    path("short-url/create/", views.CreateShortURL.as_view(), name="create-short-url"),
    path(
        "short-url/create/done/<str:code>/",
        views.CreateShortURLDone.as_view(),
        name="create-short-url-done",
    ),
    path("short-url/list/", views.ListShortURL.as_view(), name="list-short-url"),
]
