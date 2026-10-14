from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from django.db import connection

from .views import home


def database_check(request):
    return HttpResponse(
        f"Database: {connection.vendor}",
        content_type="text/plain",
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("database-check/", database_check, name="database_check"),
    path("", home, name="home"),
    path("accounts/", include("accounts.urls")),
    path("teams/", include("teams.urls")),
    path("tournaments/", include("tournaments.urls")),
    path("matches/", include("matches.urls")),
]