from django.contrib.auth.models import User
from django.db import models

from teams.models import Team


class Tournament(models.Model):
    STATUS_CHOICES = [
        ("registration", "Идёт регистрация"),
        ("started", "Турнир начался"),
        ("finished", "Завершён"),
    ]

    TEAM_SIZE_CHOICES = [
        (1, "1 игрок"),
        (2, "2 игрока"),
        (3, "3 игрока"),
        (4, "4 игрока"),
        (5, "5 игроков"),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name="Название турнира"
    )

    game = models.CharField(
        max_length=100,
        verbose_name="Игра"
    )

    rules = models.TextField(
        verbose_name="Правила"
    )

    tournament_date = models.DateTimeField(
        verbose_name="Дата проведения"
    )

    team_size = models.PositiveIntegerField(
        choices=TEAM_SIZE_CHOICES,
        verbose_name="Размер команды"
    )

    max_teams = models.PositiveIntegerField(
        default=8,
        verbose_name="Максимальное количество команд"
    )

    registration_deadline = models.DateTimeField(
        verbose_name="Дедлайн регистрации"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="registration",
        verbose_name="Статус"
    )

    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="organized_tournaments",
        verbose_name="Организатор"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class TournamentRegistration(models.Model):
    STATUS_CHOICES = [
        ("pending", "На рассмотрении"),
        ("accepted", "Принята"),
        ("rejected", "Отклонена"),
    ]

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name="registrations"
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="tournament_registrations"
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
        constraints = [
            models.UniqueConstraint(
                fields=["tournament", "team"],
                name="unique_tournament_team"
            )
        ]

    def __str__(self):
        return f"{self.team.name} — {self.tournament.name}"