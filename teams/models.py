from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    captain = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="captained_teams"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидает"),
        ("accepted", "Принят"),
        ("rejected", "Отклонён"),
    ]

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="members"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="team_memberships"
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
                fields=["team", "user"],
                name="unique_team_user"
            )
        ]

    def __str__(self):
        return f"{self.team.name} — {self.user.username}"