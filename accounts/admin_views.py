
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from teams.models import Team


@login_required
def manage_users(request):
    profile = getattr(request.user, "profile", None)

    if profile is None or profile.role != "admin":
        return render(request, "accounts/access_denied.html", status=403)

    users = User.objects.select_related("profile").order_by("username")

    return render(request, "accounts/manage_users.html", {"users": users})


@login_required
@require_POST
def change_user_role(request, user_id):
    profile = getattr(request.user, "profile", None)

    if profile is None or profile.role != "admin":
        return render(request, "accounts/access_denied.html", status=403)

    user = get_object_or_404(User, pk=user_id)

    if user.pk == request.user.pk or user.is_superuser:
        messages.error(request, "Нельзя менять роль этого аккаунта.")
        return redirect("manage_users")

    target_profile = getattr(user, "profile", None)

    if target_profile is None:
        messages.error(request, "У пользователя отсутствует профиль.")
        return redirect("manage_users")

    if target_profile.role == "admin":
        messages.error(request, "Нельзя менять роль другого администратора.")
        return redirect("manage_users")

    new_role = request.POST.get("role")
    allowed_roles = ["player", "organizer", "admin"]

    if new_role not in allowed_roles:
        messages.error(request, "Выбрана неизвестная роль.")
        return redirect("manage_users")

    target_profile.role = new_role
    target_profile.save()

    messages.success(
        request,
        f"Роль пользователя {user.username} изменена.",
    )
    return redirect("manage_users")


@login_required
@require_POST
def delete_user(request, user_id):
    profile = getattr(request.user, "profile", None)

    if profile is None or profile.role != "admin":
        return render(request, "accounts/access_denied.html", status=403)

    user = get_object_or_404(User, pk=user_id)

    if user.pk == request.user.pk:
        messages.error(request, "Нельзя удалить собственный аккаунт.")
        return redirect("manage_users")

    if user.is_superuser:
        messages.error(request, "Нельзя удалить суперпользователя.")
        return redirect("manage_users")

    target_profile = getattr(user, "profile", None)

    if target_profile and target_profile.role == "admin":
        messages.error(request, "Нельзя удалить другого администратора.")
        return redirect("manage_users")

    username = user.username

    try:
        with transaction.atomic():
            # Удаляем команды, где пользователь является капитаном.
            Team.objects.filter(captain=user).delete()

            # Затем удаляем аккаунт.
            user.delete()

    except ProtectedError:
        messages.error(
            request,
            f"Пользователь {username} не удалён: существуют другие "
            "защищённые связи с данными проекта. Аккаунт и изменения "
            "этой операции сохранены без частичного удаления. "
            "Нужно проверить модели турниров и связанных записей.",
        )
        return redirect("manage_users")

    messages.success(
        request,
        f"Пользователь {username} и его команды, где он был капитаном, удалены.",
    )
    return redirect("manage_users")
