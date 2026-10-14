from django.contrib import admin
from django.urls import include, path

from .views import home


urlpatterns = [
    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        home,
        name="home"
    ),

    path(
        "accounts/",
        include("accounts.urls")
    ),

    path(
        "teams/",
        include("teams.urls")
    ),

    path(
        "tournaments/",
        include("tournaments.urls")
    ),

    path(
        "matches/",
        include("matches.urls")
    ),
]