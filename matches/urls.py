from django.urls import path

from .views import (
    match_result,
    tournament_bracket,
)


urlpatterns = [

    path(
        "<int:tournament_id>/",
        tournament_bracket,
        name="tournament_bracket"
    ),

    path(
        "match/<int:match_id>/result/",
        match_result,
        name="match_result"
    ),

]