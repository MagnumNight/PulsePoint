from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import requests

from django.core.mail import send_mail
from .forms import UserRegisterForm
from .tokens import account_activation_token

API_ENDPOINT_URL = "https://zenquotes.io/api"


def root_homepage(request):
    return render(request, "homepage.html")


def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)

            mail_subject = "Activate your PulsePoint account."
            message = render_to_string(
                "acc_active_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return render(request, "registration/email_confirmation.html")
    else:
        form = UserRegisterForm()
    return render(request, "registration/signup.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        quote = requests.get(API_ENDPOINT_URL + "/today").json()
        messages.success(
            request,
            "Thank you for your email confirmation. Now you will be redirected to the "
            "questionnaire.",
        )
        
        # Here will be testing zenquotes API for inspirational quotes code.
        
        mail_subject = "Inspirational Quote of the Day."
        message = render_to_string(
                "quote_of_the_day.html",
                {
                    "user": user,
                    "quote": quote
                },
            )
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()



        return redirect("moodtracker:questionnaire")  # Redirect to questionnaire view
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect("root_home")


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
    if request.method == "POST":
        form = UserRegisterForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your information has been successfully updated.")
            return redirect("account_settings")
    else:
        form = UserRegisterForm(instance=request.user)
    return render(request, "registration/settings.html", {"form": form})


def send_email(request):
    if request.method == "POST":
        subject = "Support Message from PulsePoint"
        message = request.POST["message"]
        from_email = request.POST["email"]
        recipient_list = ["pulsepointregister@gmail.com"]

        send_mail(subject, message, from_email, recipient_list)

        return redirect("thank_you")


def thank_you(request):
    return render(request, "registration/thank_you.html")
