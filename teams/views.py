from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TeamCreateForm, TeamMemberInviteForm
from .models import Team, TeamMember


@login_required
def team_list(request):
    # Команды, где пользователь является капитаном
    captain_teams = Team.objects.filter(
        captain=request.user
    )

    # Команды, где пользователь является принятым участником
    member_teams = Team.objects.filter(
        members__user=request.user,
        members__status="accepted"
    )

    # Объединяем оба списка
    teams = (captain_teams | member_teams).distinct()

    return render(
        request,
        "teams/team_list.html",
        {
            "teams": teams,
        }
    )


@login_required
def team_detail(request, team_id):
    team = get_object_or_404(
        Team,
        id=team_id
    )

    # Проверяем, является ли пользователь капитаном
    is_captain = team.captain == request.user

    # Проверяем, является ли пользователь принятым участником
    is_member = team.members.filter(
        user=request.user,
        status="accepted"
    ).exists()

    # Если пользователь не капитан и не участник,
    # доступ к команде запрещён
    if not is_captain and not is_member:
        return redirect("team_list")

    members = team.members.select_related("user").all()

    return render(
        request,
        "teams/team_detail.html",
        {
            "team": team,
            "members": members,
            "is_captain": is_captain,
        }
    )


@login_required
def team_invite(request, team_id):
    # Приглашать может только капитан
    team = get_object_or_404(
        Team,
        id=team_id,
        captain=request.user
    )

    if request.method == "POST":
        form = TeamMemberInviteForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data["username"]

            if user == request.user:
                form.add_error(
                    "username",
                    "Нельзя добавить самого себя — вы уже капитан."
                )

            elif team.members.filter(user=user).exists():
                form.add_error(
                    "username",
                    "Этот пользователь уже добавлен в команду."
                )

            else:
                team.members.create(
                    user=user,
                    status="pending"
                )

                return redirect(
                    "team_detail",
                    team_id=team.id
                )

    else:
        form = TeamMemberInviteForm()

    return render(
        request,
        "teams/team_invite.html",
        {
            "team": team,
            "form": form,
        }
    )


@login_required
def my_invitations(request):
    invitations = TeamMember.objects.filter(
        user=request.user,
        status="pending"
    ).select_related(
        "team",
        "team__captain"
    )

    return render(
        request,
        "teams/my_invitations.html",
        {
            "invitations": invitations,
        }
    )


@login_required
def accept_invitation(request, member_id):
    if request.method != "POST":
        return redirect("my_invitations")

    membership = get_object_or_404(
        TeamMember,
        id=member_id,
        user=request.user,
        status="pending"
    )

    membership.status = "accepted"
    membership.save()

    return redirect("my_invitations")


@login_required
def reject_invitation(request, member_id):
    if request.method != "POST":
        return redirect("my_invitations")

    membership = get_object_or_404(
        TeamMember,
        id=member_id,
        user=request.user,
        status="pending"
    )

    membership.status = "rejected"
    membership.save()

    return redirect("my_invitations")


@login_required
def remove_member(request, member_id):
    # Удаление должно выполняться только через POST
    if request.method != "POST":
        return redirect("team_list")

    membership = get_object_or_404(
        TeamMember,
        id=member_id,
        status="accepted"
    )

    # Только капитан команды может удалить участника
    if membership.team.captain != request.user:
        return redirect("team_list")

    team_id = membership.team.id

    membership.delete()

    return redirect(
        "team_detail",
        team_id=team_id
    )


@login_required
def leave_team(request, team_id):
    # Выход из команды только через POST
    if request.method != "POST":
        return redirect("team_list")

    team = get_object_or_404(
        Team,
        id=team_id
    )

    # Капитан не может выйти из своей команды
    if team.captain == request.user:
        return redirect(
            "team_detail",
            team_id=team.id
        )

    # Находим принятого участника
    membership = get_object_or_404(
        TeamMember,
        team=team,
        user=request.user,
        status="accepted"
    )

    # Удаляем его из команды
    membership.delete()

    return redirect("team_list")


@login_required
def team_create(request):
    if request.method == "POST":
        form = TeamCreateForm(request.POST)

        if form.is_valid():
            team = form.save(commit=False)
            team.captain = request.user
            team.save()

            return redirect("team_list")

    else:
        form = TeamCreateForm()

    return render(
        request,
        "teams/team_create.html",
        {
            "form": form,
        }
    )


@login_required
def team_edit(request, team_id):
    # Изменять команду может только капитан
    team = get_object_or_404(
        Team,
        id=team_id,
        captain=request.user
    )

    if request.method == "POST":
        form = TeamCreateForm(
            request.POST,
            instance=team
        )

        if form.is_valid():
            form.save()

            return redirect("team_list")

    else:
        form = TeamCreateForm(
            instance=team
        )

    return render(
        request,
        "teams/team_edit.html",
        {
            "form": form,
            "team": team,
        }
    )


@login_required
def team_delete(request, team_id):
    # Удалять команду может только капитан
    team = get_object_or_404(
        Team,
        id=team_id,
        captain=request.user
    )

    if request.method == "POST":
        team.delete()

        return redirect("team_list")

    return render(
        request,
        "teams/team_delete.html",
        {
            "team": team,
        }
    )