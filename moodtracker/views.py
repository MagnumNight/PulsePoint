import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Questionnaire, MoodData
from .forms import QuestionnaireForm, MoodDataForm
import plotly.express as px
import plotly.offline as opy
import pandas as pd


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
                    "happiness_level": form.cleaned_data["happiness_level"],
                    "stress_level": form.cleaned_data["stress_level"],
                    "relaxation_level": form.cleaned_data["relaxation_level"],
                    "energy_level": form.cleaned_data["energy_level"],
                    "creativity_level": form.cleaned_data["creativity_level"],
                    "focus_level": form.cleaned_data["focus_level"],
                    "social_level": form.cleaned_data["social_level"],
                    "motivation_level": form.cleaned_data["motivation_level"],
                    "confidence_level": form.cleaned_data["confidence_level"],
                    "contentment_level": form.cleaned_data["contentment_level"],
                },
            )
            if created:
                messages.success(request, "Your mood has been recorded!")
            else:
                messages.info(request, "Your mood for today has been updated!")
            return redirect("moodtracker:home")
    else:
        form = MoodDataForm()

    return render(request, "moodtracker/save_mood.html", {"form": form})


@login_required
def mood_graph_view(request):
    mood_data = MoodData.objects.filter(user=request.user).order_by("date")
    mood_dates = [data.date.strftime("%Y-%m-%d") for data in mood_data]

    # Collecting all mood data
    mood_metrics = {
        "Happiness": [data.happiness_level for data in mood_data],
        "Stress": [data.stress_level for data in mood_data],
        "Relaxation": [data.relaxation_level for data in mood_data],
        "Energy": [data.energy_level for data in mood_data],
        "Creativity": [data.creativity_level for data in mood_data],
        "Focus": [data.focus_level for data in mood_data],
        "Social": [data.social_level for data in mood_data],
        "Motivation": [data.motivation_level for data in mood_data],
        "Confidence": [data.confidence_level for data in mood_data],
        "Contentment": [data.contentment_level for data in mood_data],
    }

    # Define colors for each mood
    colors = {
        "Happiness": "green",
        "Stress": "red",
        "Relaxation": "blue",
        "Energy": "yellow",
        "Creativity": "purple",
        "Focus": "cyan",
        "Social": "orange",
        "Motivation": "pink",
        "Confidence": "gold",
        "Contentment": "brown",
    }

    # Dictionary to hold individual plot divs
    plot_divs = {}

    for metric in mood_metrics.keys():
        metric_data = {metric: mood_metrics[metric], "Date": mood_dates}
        df_metric = pd.DataFrame(metric_data)

        fig = px.bar(
            df_metric,
            x="Date",
            y=metric,
            title=f"Your {metric} Levels Over Time",
            color_discrete_sequence=[colors.get(metric, "grey")],
        )

        fig.update_layout(
            title={
                "text": f"Your {metric} Levels Over Time",
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
                "font": {"size": 24},
            }
        )

        fig.update_yaxes(
            tickvals=[1, 2, 3, 4, 5],
            ticktext=[
                "Not at all",
                "Not really",
                "Neutral",
                "Somewhat",
                "Completely",
            ],
        )

        fig.update_xaxes(
            type="category"
        )

        plot_divs[metric] = opy.plot(fig, output_type="div", include_plotlyjs=False)

    context = {
        "plot_divs": plot_divs,
    }

    return render(request, "moodtracker/mood_graph.html", context)
