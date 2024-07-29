from django.urls import path
from . import views

urlpatterns = [
    path("ping", views.ping),
    path("all-coins", views.listAllCoins),
    path("coin-details", views.getCoinDetails),
]
