from .forms import UserRegisterForm
from django.shortcuts import render, redirect
from django.contrib import messages


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
