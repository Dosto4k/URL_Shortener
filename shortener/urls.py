from django.urls import path

from shortener import views


app_name = "shortener"
urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
]
