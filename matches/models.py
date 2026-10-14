from django.db import models

from teams.models import Team
from tournaments.models import Tournament


class Match(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидает результата"),
        ("finished", "Завершён"),
    ]

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name="matches"
    )

    round_number = models.PositiveIntegerField(
        default=1,
        verbose_name="Раунд"
    )

    match_number = models.PositiveIntegerField(
        default=1,
        verbose_name="Номер матча"
    )

    team1 = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="matches_as_team1",
        null=True,
        blank=True
    )

    team2 = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="matches_as_team2",
        null=True,
        blank=True
    )

    score1 = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    score2 = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    winner = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name="won_matches",
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            "round_number",
            "match_number"
        ]

    def __str__(self):
        team1_name = (
            self.team1.name
            if self.team1
            else "Ожидается"
        )

        team2_name = (
            self.team2.name
            if self.team2
            else "Ожидается"
        )

        return (
            f"{self.tournament.name}: "
            f"{team1_name} — {team2_name}"
        )