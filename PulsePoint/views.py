from .forms import UserRegisterForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def root_homepage(request):
    return render(request, "homepage.html")


def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Account created for {username}! You can now login."
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been successfully deleted.")
        return redirect("root_home")
    return render(request, "registration/delete_account.html")


@login_required
def account_settings(request):
    form = UserRegisterForm(instance=request.user)
    return render(request, "registration/settings.html", {"form": form})


@login_required
def update_information(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your information has been successfully updated.")
            return redirect("account_settings")
    else:
        form = UserRegisterForm(instance=request.user)

    return render(request, "registration/settings.html", {"form": form})
