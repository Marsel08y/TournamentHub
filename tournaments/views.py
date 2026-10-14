import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from matches.models import Match
from teams.models import Team

from .forms import (
    TournamentCreateForm,
    TournamentRegistrationForm,
)
from .models import (
    Tournament,
    TournamentRegistration,
)


@login_required
def tournament_list(request):
    tournaments = Tournament.objects.all().order_by("-created_at")

    return render(
        request,
        "tournaments/tournament_list.html",
        {"tournaments": tournaments},
    )


@login_required
def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(
        Tournament,
        id=tournament_id,
    )

    registration = TournamentRegistration.objects.filter(
        tournament=tournament,
        team__captain=request.user,
    ).first()

    registrations = (
        TournamentRegistration.objects.filter(tournament=tournament)
        .select_related("team", "team__captain")
        .prefetch_related("team__members__user")
        .order_by("-created_at")
    )

    user_teams = Team.objects.filter(
        captain=request.user,
    ).order_by("name")

    is_organizer = request.user.pk == tournament.organizer_id

    return render(
        request,
        "tournaments/tournament_detail.html",
        {
            "tournament": tournament,
            "registration": registration,
            "registrations": registrations,
            "user_teams": user_teams,
            "is_organizer": is_organizer,
        },
    )


@login_required
def tournament_create(request):
    # Создавать турниры может любой вошедший пользователь.
    if request.method == "POST":
        form = TournamentCreateForm(request.POST)

        if form.is_valid():
            tournament = form.save(commit=False)
            tournament.organizer = request.user
            tournament.save()

            messages.success(
                request,
                "Турнир успешно создан!",
            )

            return redirect(
                "tournament_detail",
                tournament_id=tournament.id,
            )

    else:
        form = TournamentCreateForm()

    return render(
        request,
        "tournaments/tournament_create.html",
        {"form": form},
    )


@login_required
def tournament_register(request, tournament_id):
    tournament = get_object_or_404(
        Tournament,
        id=tournament_id,
    )

    if tournament.status != "registration":
        messages.error(
            request,
            "Регистрация на этот турнир уже закрыта.",
        )

        return redirect(
            "tournament_detail",
            tournament_id=tournament.id,
        )

    if request.method == "POST":
        form = TournamentRegistrationForm(
            request.user,
            tournament,
            request.POST,
        )

        if form.is_valid():
            team = form.cleaned_data["team"]

            TournamentRegistration.objects.create(
                tournament=tournament,
                team=team,
            )

            messages.success(
                request,
                f"Команда «{team.name}» успешно зарегистрирована "
                f"на турнир!",
            )

            return redirect(
                "tournament_detail",
                tournament_id=tournament.id,
            )

    else:
        form = TournamentRegistrationForm(
            request.user,
            tournament,
        )

    return render(
        request,
        "tournaments/tournament_register.html",
        {
            "tournament": tournament,
            "form": form,
        },
    )


@login_required
def tournament_applications(request, tournament_id):
    tournament = get_object_or_404(
        Tournament,
        id=tournament_id,
        organizer=request.user,
    )

    registrations = (
        TournamentRegistration.objects.filter(tournament=tournament)
        .select_related("team", "team__captain")
        .prefetch_related("team__members__user")
        .order_by("-created_at")
    )

    return render(
        request,
        "tournaments/tournament_applications.html",
        {
            "tournament": tournament,
            "registrations": registrations,
        },
    )


@login_required
def accept_tournament_registration(request, registration_id):
    if request.method != "POST":
        return redirect("tournament_list")

    registration = get_object_or_404(
        TournamentRegistration,
        id=registration_id,
        tournament__organizer=request.user,
    )

    registration.status = "accepted"
    registration.save()

    messages.success(
        request,
        f"Команда «{registration.team.name}» принята в турнир.",
    )

    return redirect(
        "tournament_applications",
        tournament_id=registration.tournament.id,
    )


@login_required
def reject_tournament_registration(request, registration_id):
    if request.method != "POST":
        return redirect("tournament_list")

    registration = get_object_or_404(
        TournamentRegistration,
        id=registration_id,
        tournament__organizer=request.user,
    )

    registration.status = "rejected"
    registration.save()

    messages.success(
        request,
        f"Заявка команды «{registration.team.name}» отклонена.",
    )

    return redirect(
        "tournament_applications",
        tournament_id=registration.tournament.id,
    )


@login_required
def remove_team_from_tournament(request, registration_id):
    if request.method != "POST":
        return redirect("tournament_list")

    registration = get_object_or_404(
        TournamentRegistration,
        id=registration_id,
        tournament__organizer=request.user,
    )

    tournament_id = registration.tournament.id
    team_name = registration.team.name

    registration.delete()

    messages.success(
        request,
        f"Команда «{team_name}» удалена из турнира.",
    )

    return redirect(
        "tournament_applications",
        tournament_id=tournament_id,
    )


@login_required
def tournament_edit(request, tournament_id):
    tournament = get_object_or_404(
        Tournament,
        id=tournament_id,
        organizer=request.user,
    )

    if request.method == "POST":
        form = TournamentCreateForm(
            request.POST,
            instance=tournament,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Турнир успешно изменён.",
            )

            return redirect(
                "tournament_detail",
                tournament_id=tournament.id,
            )

    else:
        form = TournamentCreateForm(
            instance=tournament,
        )

    return render(
        request,
        "tournaments/tournament_edit.html",
        {
            "form": form,
            "tournament": tournament,
        },
    )


@login_required
def tournament_delete(request, tournament_id):
    tournament = get_object_or_404(
        Tournament,
        id=tournament_id,
        organizer=request.user,
    )

    if request.method == "POST":
        tournament_name = tournament.name
        tournament.delete()

        messages.success(
            request,
            f"Турнир «{tournament_name}» удалён.",
        )

        return redirect("tournament_list")

    return render(
        request,
        "tournaments/tournament_delete.html",
        {"tournament": tournament},
    )


@login_required
def tournament_draw(request, tournament_id):
    tournament = get_object_or_404(
        Tournament,
        id=tournament_id,
        organizer=request.user,
    )

    if request.method != "POST":
        return redirect(
            "tournament_detail",
            tournament_id=tournament.id,
        )

    if tournament.status != "registration":
        messages.error(
            request,
            "Жеребьёвку уже нельзя провести.",
        )

        return redirect(
            "tournament_detail",
            tournament_id=tournament.id,
        )

    if Match.objects.filter(tournament=tournament).exists():
        messages.error(
            request,
            "Жеребьёвка для этого турнира уже проведена.",
        )

        return redirect(
            "tournament_bracket",
            tournament_id=tournament.id,
        )

    registrations = (
        TournamentRegistration.objects.filter(
            tournament=tournament,
            status="accepted",
        )
        .select_related("team")
    )

    teams = [
        registration.team
        for registration in registrations
    ]

    if len(teams) < 2:
        messages.error(
            request,
            "Для жеребьёвки необходимо минимум 2 принятые команды.",
        )

        return redirect(
            "tournament_applications",
            tournament_id=tournament.id,
        )

    if len(teams) > tournament.max_teams:
        teams = teams[:tournament.max_teams]

    random.shuffle(teams)

    match_number = 1

    for i in range(0, len(teams), 2):
        team1 = teams[i]

        if i + 1 < len(teams):
            team2 = teams[i + 1]

            Match.objects.create(
                tournament=tournament,
                round_number=1,
                match_number=match_number,
                team1=team1,
                team2=team2,
                status="pending",
            )
        else:
            Match.objects.create(
                tournament=tournament,
                round_number=1,
                match_number=match_number,
                team1=team1,
                team2=None,
                winner=team1,
                status="finished",
            )

        match_number += 1

    tournament.status = "started"
    tournament.save()

    messages.success(
        request,
        "Жеребьёвка успешно проведена! Сетка турнира создана.",
    )

    return redirect(
        "tournament_bracket",
        tournament_id=tournament.id,
    )
