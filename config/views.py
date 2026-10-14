from django.shortcuts import render

from tournaments.models import TournamentRegistration


def home(request):
    my_registrations = []

    if request.user.is_authenticated:
        my_registrations = TournamentRegistration.objects.filter(
            team__captain=request.user
        ).select_related(
            "tournament",
            "team"
        ).order_by("-created_at")

    recent_registrations = TournamentRegistration.objects.filter(
        status="accepted"
    ).select_related(
        "tournament",
        "team",
        "team__captain"
    ).order_by("-created_at")[:5]

    return render(
        request,
        "home.html",
        {
            "my_registrations": my_registrations,
            "recent_registrations": recent_registrations,
        }
    )