from django.urls import path

from shortener import views


app_name = "shortener"
urlpatterns = [
    path("", views.CreateShortUrlView.as_view(), name="create-short-url"),
]
