from .forms import UserRegisterForm
from moodtracker.forms import QuestionnaireForm
from moodtracker.models import Questionnaire
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


def root_homepage(request):
    return render(request, "homepage.html")


def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user = form.save()
            username = form.cleaned_data.get("username")
            current_site = get_current_site(request)
            login(request, user)  # Log in the user
            #messages.success(request, form.errors)

            mail_subject = 'Activate your PulsePoint account.'
            
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
            
            #return redirect("root_home")
        messages.success(request, form.errors)
        # Will need to add an error message on the specific case where the user made their mistake
        #I.E. Password complexity
        print(form.errors)
    form = UserRegisterForm()
    return render(request, "registration/signup.html", {"form": form})

def activate(request, uidb64, token):
    form = UserRegisterForm(request.POST)
    #questionnaire = Questionnaire.objects.get(user=request.user)
    context = {
        'uidb64': uidb64,
         'token': token
         } 
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Thank you for your email confirmation. Please complete our questionnaire")

        return render(request, "registration/questionnaire.html", {"form": form})

        if request.method == "POST":
            form = QuestionnaireForm(request.POST)
            if form.is_valid():
                questionnaire = form.save(commit=False)
                questionnaire.user = request.user
                questionnaire.save()
                messages.success(
                    request, "Your questionnaire has been submitted successfully!"
                )
                return redirect("moodtracker:home")
        else:
            form = QuestionnaireForm()        
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        messages.success(
                    request, "Your questionnaire has been submitted successfully! Welcome to PulsePoint!"
                )
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
