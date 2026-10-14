from django.urls import path

from .views import (
    accept_tournament_registration,
    reject_tournament_registration,
    remove_team_from_tournament,
    tournament_applications,
    tournament_create,
    tournament_delete,
    tournament_detail,
    tournament_draw,
    tournament_edit,
    tournament_list,
    tournament_register,
)


urlpatterns = [
    path(
        "",
        tournament_list,
        name="tournament_list"
    ),

    path(
        "create/",
        tournament_create,
        name="tournament_create"
    ),

    path(
        "<int:tournament_id>/register/",
        tournament_register,
        name="tournament_register"
    ),

    path(
        "<int:tournament_id>/applications/",
        tournament_applications,
        name="tournament_applications"
    ),

    path(
        "applications/<int:registration_id>/accept/",
        accept_tournament_registration,
        name="accept_tournament_registration"
    ),

    path(
        "applications/<int:registration_id>/reject/",
        reject_tournament_registration,
        name="reject_tournament_registration"
    ),

    path(
        "applications/<int:registration_id>/remove/",
        remove_team_from_tournament,
        name="remove_team_from_tournament"
    ),

    path(
        "<int:tournament_id>/draw/",
        tournament_draw,
        name="tournament_draw"
    ),

    path(
        "<int:tournament_id>/edit/",
        tournament_edit,
        name="tournament_edit"
    ),

    path(
        "<int:tournament_id>/delete/",
        tournament_delete,
        name="tournament_delete"
    ),

    path(
        "<int:tournament_id>/",
        tournament_detail,
        name="tournament_detail"
    ),
]