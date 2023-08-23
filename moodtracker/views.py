from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Questionnaire
from .forms import QuestionnaireForm


@login_required
def home(request):
    return render(request, "moodtracker/home.html")


@login_required
def questionnaire_view(request):
    try:
        questionnaire = Questionnaire.objects.get(user=request.user)
        if questionnaire:
            messages.info(request, "You have already filled out the questionnaire.")
            return redirect("moodtracker:home")
    except Questionnaire.DoesNotExist:
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

        return render(request, "moodtracker/questionnaire.html", {"form": form})
