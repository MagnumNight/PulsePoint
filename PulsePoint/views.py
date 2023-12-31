from importlib import import_module
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import UserRegisterForm, UserSettingsForm, PasswordResetForm
from .tokens import account_activation_token, password_reset_token
from django.contrib.auth.signals import user_logged_in
from django.contrib.sessions.models import Session
from django.dispatch import receiver
from django.utils import timezone
import requests

API_ENDPOINT_URL = "https://zenquotes.io/api"


# Function: root_homepage - Renders homepage
def root_homepage(request):
    url = requests.get(API_ENDPOINT_URL + "/today").json()
    data = url

    if data:
        quote = data[0][
            "q"
        ]  # Assuming the quote is stored under key 'q' in the API response
    else:
        quote = "Unable to fetch a quote at the moment."
    return render(request, "homepage.html", {"quote": quote})


# Function: signup - Renders signup page
def signup(request):
    # If user submits signup form, save user and send activation email
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
    # If user does not submit signup form, go back to signup page
    else:
        form = UserRegisterForm()
    return render(request, "registration/signup.html", {"form": form})


# Function: activate - Activates user account
def activate(request, uidb64, token):
    # Check if user is already logged in
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # If user is logged in and token matches, activate user account
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user)
        # quote = requests.get(API_ENDPOINT_URL + "/today").json()
        messages.success(
            request,
            "Thank you for your email confirmation. Now you will be redirected to the "
            "questionnaire.",
        )
        return redirect("moodtracker:questionnaire")
    # If user is logged in, redirect to home page
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect("root_home")


@login_required
# Function: delete_account - Renders delete account page
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been successfully deleted.")
        return redirect("root_home")
    return render(request, "registration/delete_account.html")


@login_required
def update_info(request):
    if request.method == "POST":
        form = UserSettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)

            # Password change section
            current_password = form.cleaned_data.get("current_password")
            new_password1 = form.cleaned_data.get("new_password1")
            if current_password and new_password1:
                user.set_password(new_password1)

            user.save()
            update_session_auth_hash(
                request, user
            )  # Keep the user logged in after a password change

            messages.success(request, "Your information has been successfully updated.")
            return redirect("account_settings")
        else:
            # Check for non-unique email/username
            if "username" in form.errors:
                messages.error(
                    request, "The username is already in use. Please choose another."
                )
            if "email" in form.errors:
                messages.error(
                    request, "The email is already in use. Please choose another."
                )
            # Do not redirect, render the template and pass the invalid form
            return render(request, "registration/update_info.html", {"form": form})
    else:
        form = UserSettingsForm(instance=request.user)
    return render(request, "registration/update_info.html", {"form": form})


# Function: send_email - Sends registration email
def send_email(request):
    if request.method == "POST":
        subject = "Support Message from PulsePoint"
        message = request.POST["message"]
        from_email = request.POST["email"]
        recipient_list = ["pulsepointregister@gmail.com"]

        send_mail(subject, message, from_email, recipient_list)

        return redirect("thank_you")


@login_required
def account_settings(request):
    return render(request, "registration/settings.html")


# Function: thank_you - Renders thank you page
def thank_you(request):
    return render(request, "registration/thank_you.html")


# Function: about - Renders about page
def about(request):
    return render(request, "about.html")


# Function: contact - Renders contact page
def contact(request):
    return render(request, "contact.html")


# Function: password_reset_view - Renders password reset page
def password_reset_view(request):
    # If user submits password reset form, send password reset email
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(
                request,
                "error_page.html",
                {"error_message": "This email is not registered in our system."},
            )

        current_site = get_current_site(request)
        mail_subject = "Reset your password"
        message = render_to_string(
            "password_reset_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": password_reset_token.make_token(user),
            },
        )
        send_mail(mail_subject, message, "pulsepointregister@gmail.com", [email])
        return render(request, "email_sent_confirmation.html")
    return render(request, "password_reset_form.html")


# Function: password_reset_confirm - Renders password reset confirmation page
def password_reset_confirm(request, uidb64, token):
    # Check if user is already logged in
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # If user is logged in and token matches, reset password
    if user is not None and password_reset_token.check_token(user, token):
        if request.method == "POST":
            form = PasswordResetForm(request.POST, instance=user)
            if form.is_valid():
                user.set_password(form.cleaned_data["new_password1"])
                user.save()
                return redirect("password_reset_success")

        else:
            form = PasswordResetForm(instance=user)

        context = {"form": form}
        return render(request, "password_reset_confirm.html", context)

    else:
        return render(
            request,
            "error_page.html",
            {"error_message": "Password reset link is invalid or has expired."},
        )


# Function: password_reset_success - Renders password reset success page
def password_reset_success(request):
    return render(request, "password_reset_success.html")


# This should log the user out of all sessions, other than the active session
@receiver(user_logged_in)
def on_user_logged_in(request, **kwargs):
    # Get the current session key
    current_session_key = request.session.session_key

    # Get all session keys
    sessions = Session.objects.filter(expire_date__gt=timezone.now())

    # Exclude the current session and delete the rest
    for session in sessions:
        if session.session_key != current_session_key:
            # Decode session data
            engine = import_module(settings.SESSION_ENGINE)
            session_data = engine.SessionStore().decode(session.session_data)

            # Check if session data contains user's id
            if session_data.get("_auth_user_id") == str(request.user.id):
                session.delete()
