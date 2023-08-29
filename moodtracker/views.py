import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Questionnaire, MoodData
from .forms import QuestionnaireForm, MoodDataForm


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


@login_required
def save_mood(request):
    if request.method == "POST":
        form = MoodDataForm(request.POST)
        if form.is_valid():
            mood_data, created = MoodData.objects.update_or_create(
                user=request.user,
                date=datetime.date.today(),
                defaults={
                    "mood_rating": form.cleaned_data["mood_rating"],
                    "mood_emoji": form.cleaned_data.get("mood_emoji", "🙂"),
                },
            )
            if created:
                messages.success(request, "Your mood has been recorded!")
            else:
                messages.info(request, "Your mood for this date has been updated!")
            return redirect("moodtracker:home")
    else:
        form = MoodDataForm()

    return render(request, "moodtracker/save_mood.html", {"form": form})


# New view for mood graph
@login_required
def mood_graph_view(request):
    # For now, just rendering a placeholder template.
    return render(request, "moodtracker/mood_graph.html")
