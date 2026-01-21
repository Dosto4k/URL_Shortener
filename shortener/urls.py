from django.urls import path

from shortener import views


app_name = "shortener"
urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path("shortener/", views.CreateShortURL.as_view(), name="create-short-url"),
    path(
        "shortener/done/<str:code>/",
        views.CreateShortURLDone.as_view(),
        name="create-short-url-done",
    ),
]
