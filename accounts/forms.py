from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email"
    )

    first_name = forms.CharField(
        max_length=150,
        required=True,
        label="Имя"
    )

    last_name = forms.CharField(
        max_length=150,
        required=True,
        label="Фамилия"
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()

            Profile.objects.create(
                user=user,
                role="player"
            )

        return user