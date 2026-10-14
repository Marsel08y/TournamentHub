from django import forms
from django.contrib.auth.models import User

from .models import Team


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name"]

        labels = {
            "name": "Название команды",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Например: Cyber Wolves",
                }
            ),
        }


class TeamMemberInviteForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Имя пользователя",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите username игрока",
            }
        ),
    )

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(
                "Пользователь с таким username не найден."
            )

        return user