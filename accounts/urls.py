
from django.urls import path

from .admin_views import change_user_role, manage_users, delete_user
from .views import login_view, logout_view, profile_view, register_view


urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("manage-users/", manage_users, name="manage_users"),
    path(
        "manage-users/<int:user_id>/role/",
        change_user_role,
        name="change_user_role",
    ),
    path(
        "manage-users/<int:user_id>/delete/",
        delete_user,
        name="user_delete",
    ),
]
