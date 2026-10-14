from django import forms

from .models import Match


class MatchResultForm(forms.ModelForm):

    class Meta:
        model = Match

        fields = [
            "score1",
            "score2",
        ]

        labels = {
            "score1": "Счёт первой команды",
            "score2": "Счёт второй команды",
        }

        widgets = {
            "score1": forms.NumberInput(
                attrs={
                    "min": 0,
                    "placeholder": "Например: 2",
                }
            ),
            "score2": forms.NumberInput(
                attrs={
                    "min": 0,
                    "placeholder": "Например: 1",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        score1 = cleaned_data.get("score1")
        score2 = cleaned_data.get("score2")

        if score1 is None or score2 is None:
            return cleaned_data

        if score1 == score2:
            raise forms.ValidationError(
                "Ничья недопустима. Укажите победителя."
            )

        return cleaned_data