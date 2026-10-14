from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import RegisterForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "Регистрация прошла успешно!"
            )

            return redirect("home")
    else:
        form = RegisterForm()

    return render(
        request,
        "registration/register.html",
        {"form": form}
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(
                request,
                "Вы успешно вошли!"
            )

            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(
        request,
        "registration/login.html",
        {"form": form}
    )


@login_required
def logout_view(request):
    logout(request)

    messages.success(
        request,
        "Вы вышли из аккаунта."
    )

    return redirect("home")


@login_required
def profile_view(request):
    return render(
        request,
        "accounts/profile.html"
    )