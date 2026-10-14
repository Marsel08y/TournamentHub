from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from tournaments.models import Tournament
from .forms import MatchResultForm
from .models import Match


@login_required
def tournament_bracket(request, tournament_id):
    tournament = get_object_or_404(
        Tournament,
        id=tournament_id
    )

    matches = Match.objects.filter(
        tournament=tournament
    ).select_related(
        "team1",
        "team2",
        "winner"
    )

    rounds = {}

    for match in matches:
        if match.round_number not in rounds:
            rounds[match.round_number] = []

        rounds[match.round_number].append(match)

    champion = None

    if tournament.status == "finished":
        last_round_number = Match.objects.filter(
            tournament=tournament
        ).order_by("-round_number").values_list(
            "round_number",
            flat=True
        ).first()

        if last_round_number is not None:
            final_match = Match.objects.filter(
                tournament=tournament,
                round_number=last_round_number
            ).order_by("-match_number").first()

            if final_match and final_match.winner:
                champion = final_match.winner

    is_organizer = request.user.pk == tournament.organizer_id

    return render(
        request,
        "matches/tournament_bracket.html",
        {
            "tournament": tournament,
            "rounds": rounds,
            "is_organizer": is_organizer,
            "champion": champion,
        }
    )


@login_required
def match_result(request, match_id):
    match = get_object_or_404(
        Match.objects.select_related(
            "tournament",
            "team1",
            "team2",
            "winner"
        ),
        id=match_id
    )

    tournament = match.tournament

    if request.user.pk != tournament.organizer_id:
        messages.error(
            request,
            "Только организатор турнира может вводить результаты."
        )

        return redirect(
            "tournament_bracket",
            tournament_id=tournament.id
        )

    if match.status == "finished":
        messages.error(
            request,
            "Этот матч уже завершён."
        )

        return redirect(
            "tournament_bracket",
            tournament_id=tournament.id
        )

    if match.team1 is None or match.team2 is None:
        messages.error(
            request,
            "Для этого матча результат вводить не нужно."
        )

        return redirect(
            "tournament_bracket",
            tournament_id=tournament.id
        )

    if request.method == "POST":
        form = MatchResultForm(
            request.POST,
            instance=match
        )

        if form.is_valid():
            score1 = form.cleaned_data["score1"]
            score2 = form.cleaned_data["score2"]

            match.score1 = score1
            match.score2 = score2

            if score1 > score2:
                match.winner = match.team1
            else:
                match.winner = match.team2

            match.status = "finished"
            match.save()

            current_round = match.round_number

            current_round_matches = Match.objects.filter(
                tournament=tournament,
                round_number=current_round
            ).order_by("match_number")

            pending_matches = current_round_matches.filter(
                status="pending"
            )

            if not pending_matches.exists():
                winners = []

                for current_match in current_round_matches:
                    if current_match.winner:
                        winners.append(current_match.winner)

                if len(winners) == 1:
                    tournament.status = "finished"
                    tournament.save()

                    messages.success(
                        request,
                        f"🏆 Турнир завершён! "
                        f"Победитель: «{winners[0].name}»."
                    )

                elif len(winners) >= 2:
                    next_round = current_round + 1

                    existing_next_round = Match.objects.filter(
                        tournament=tournament,
                        round_number=next_round
                    ).exists()

                    if not existing_next_round:
                        match_number = 1

                        for i in range(0, len(winners), 2):
                            team1 = winners[i]

                            if i + 1 < len(winners):
                                team2 = winners[i + 1]

                                Match.objects.create(
                                    tournament=tournament,
                                    round_number=next_round,
                                    match_number=match_number,
                                    team1=team1,
                                    team2=team2,
                                    status="pending"
                                )

                            else:
                                Match.objects.create(
                                    tournament=tournament,
                                    round_number=next_round,
                                    match_number=match_number,
                                    team1=team1,
                                    team2=None,
                                    winner=team1,
                                    status="finished"
                                )

                            match_number += 1

                        messages.success(
                            request,
                            "🏆 Раунд завершён! "
                            "Победители перешли в следующий раунд."
                        )

            return redirect(
                "tournament_bracket",
                tournament_id=tournament.id
            )

    else:
        form = MatchResultForm(
            instance=match
        )

    return render(
        request,
        "matches/match_result.html",
        {
            "match": match,
            "tournament": tournament,
            "form": form,
        }
    )
