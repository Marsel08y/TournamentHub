from django import forms

from .models import Tournament, TournamentRegistration
from teams.models import Team


class TournamentCreateForm(forms.ModelForm):
    class Meta:
        model = Tournament

        fields = [
            "name",
            "game",
            "rules",
            "tournament_date",
            "team_size",
            "max_teams",
            "registration_deadline",
        ]

        labels = {
            "name": "Название турнира",
            "game": "Игра",
            "rules": "Правила",
            "tournament_date": "Дата проведения",
            "team_size": "Размер команды",
            "max_teams": "Максимальное количество команд",
            "registration_deadline": "Дедлайн регистрации",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Например: Cyber Cup 2026",
                }
            ),

            "game": forms.TextInput(
                attrs={
                    "placeholder": "Например: CS2",
                }
            ),

            "rules": forms.Textarea(
                attrs={
                    "placeholder": "Опишите правила турнира...",
                    "rows": 6,
                }
            ),

            "tournament_date": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),

            "registration_deadline": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),

            "max_teams": forms.NumberInput(
                attrs={
                    "min": 2,
                    "max": 64,
                }
            ),
        }


class TournamentRegistrationForm(forms.Form):
    team = forms.ModelChoiceField(
        queryset=Team.objects.none(),
        label="Выберите команду",
        empty_label="Выберите команду",
    )

    def __init__(self, user, tournament, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["team"].queryset = Team.objects.filter(
            captain=user
        ).order_by("name")

        self.tournament = tournament

    def clean_team(self):
        team = self.cleaned_data["team"]

        if TournamentRegistration.objects.filter(
            tournament=self.tournament,
            team=team
        ).exists():
            raise forms.ValidationError(
                "Эта команда уже зарегистрирована на данный турнир."
            )

        return team