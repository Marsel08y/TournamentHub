from django.urls import path

from .views import (
    accept_invitation,
    leave_team,
    my_invitations,
    reject_invitation,
    remove_member,
    team_create,
    team_delete,
    team_detail,
    team_edit,
    team_invite,
    team_list,
)


urlpatterns = [
    path(
        "",
        team_list,
        name="team_list"
    ),

    path(
        "create/",
        team_create,
        name="team_create"
    ),

    path(
        "invitations/",
        my_invitations,
        name="my_invitations"
    ),

    path(
        "invitations/<int:member_id>/accept/",
        accept_invitation,
        name="accept_invitation"
    ),

    path(
        "invitations/<int:member_id>/reject/",
        reject_invitation,
        name="reject_invitation"
    ),

    path(
        "members/<int:member_id>/remove/",
        remove_member,
        name="remove_member"
    ),

    path(
        "<int:team_id>/leave/",
        leave_team,
        name="leave_team"
    ),

    path(
        "<int:team_id>/",
        team_detail,
        name="team_detail"
    ),

    path(
        "<int:team_id>/edit/",
        team_edit,
        name="team_edit"
    ),

    path(
        "<int:team_id>/delete/",
        team_delete,
        name="team_delete"
    ),

    path(
        "<int:team_id>/invite/",
        team_invite,
        name="team_invite"
    ),
]