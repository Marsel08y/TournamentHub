from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render


@login_required
def manage_users(request):
    profile = getattr(request.user, "profile", None)

    if profile is None or profile.role != "admin":
        return render(
            request,
            "accounts/access_denied.html",
            status=403
        )

    users = User.objects.select_related(
        "profile"
    ).order_by("username")

    return render(
        request,
        "accounts/manage_users.html",
        {
            "users": users,
        }
    )


@login_required
def change_user_role(request, user_id):
    profile = getattr(request.user, "profile", None)

    if profile is None or profile.role != "admin":
        return render(
            request,
            "accounts/access_denied.html",
            status=403
        )

    if request.method != "POST":
        return redirect("manage_users")

    user = get_object_or_404(
        User,
        id=user_id
    )

    new_role = request.POST.get("role")

    allowed_roles = [
        "player",
        "organizer",
        "admin",
    ]

    if new_role not in allowed_roles:
        messages.error(
            request,
            "Выбрана неизвестная роль."
        )

        return redirect("manage_users")

    user_profile = getattr(user, "profile", None)

    if user_profile is None:
        messages.error(
            request,
            "У пользователя отсутствует профиль."
        )

        return redirect("manage_users")

    user_profile.role = new_role
    user_profile.save()

    messages.success(
        request,
        f"Роль пользователя {user.username} успешно изменена."
    )

    return redirect("manage_users")