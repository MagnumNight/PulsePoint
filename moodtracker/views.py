import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Questionnaire, MoodData
from .forms import QuestionnaireForm, MoodDataForm
import plotly.express as px
import plotly.offline as opy
import pandas as pd


# Function: home - Renders home page
@login_required
def home(request):
    return render(request, "moodtracker/home.html")


# Function: questionnaire_view - Renders questionnaire page
@login_required
def questionnaire_view(request):
    # Check if user has already filled out questionnaire
    try:
        questionnaire = Questionnaire.objects.get(user=request.user)
        # If user has already filled out questionnaire, redirect to home page
        if questionnaire:
            messages.info(request, "You have already filled out the questionnaire.")
            return redirect("moodtracker:home")
    # If user has not filled out questionnaire, render questionnaire page
    except Questionnaire.DoesNotExist:
        # If user submits questionnaire, save questionnaire and redirect to home page
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
        # If user does not submit questionnaire, render questionnaire page
        else:
            form = QuestionnaireForm()

        return render(request, "moodtracker/questionnaire.html", {"form": form})


# Function: save_mood - Renders save mood page
@login_required
def save_mood(request):
    # Check if user has already filled out questionnaire
    if request.method == "POST":
        form = MoodDataForm(request.POST)
        # If user submits mood data, save mood data and redirect to home page
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
            # If mood data is created, display success message
            if created:
                messages.success(request, "Your mood has been recorded!")
            # If mood data is updated, display info message
            else:
                messages.info(request, "Your mood for today has been updated!")
            return redirect("moodtracker:home")
    # If user does not submit mood data, render save mood page
    else:
        form = MoodDataForm()

    return render(request, "moodtracker/save_mood.html", {"form": form})


# Function: mood_graph_view - Renders mood graph page
@login_required
def mood_graph_view(request):
    mood_data = MoodData.objects.filter(user=request.user).order_by("date")
    mood_dates = [data.date.strftime("%Y-%m-%d") for data in mood_data]

    # Check if user has filled out questionnaire
    try:
        initial_questionnaire = Questionnaire.objects.get(user=request.user)
    except Questionnaire.DoesNotExist:
        initial_questionnaire = None

    # If user has filled out questionnaire, add initial data to mood metrics
    if initial_questionnaire:
        initial_data = {
            "Happiness": [initial_questionnaire.happiness_level],
            "Stress": [initial_questionnaire.stress_level],
            "Relaxation": [initial_questionnaire.relaxation_level],
            "Energy": [initial_questionnaire.energy_level],
            "Creativity": [initial_questionnaire.creativity_level],
            "Focus": [initial_questionnaire.focus_level],
            "Social": [initial_questionnaire.social_level],
            "Motivation": [initial_questionnaire.motivation_level],
            "Confidence": [initial_questionnaire.confidence_level],
            "Contentment": [initial_questionnaire.contentment_level],
        }

        mood_dates.insert(0, "Initial")

    # If user has not filled out questionnaire, set initial data to empty
    else:
        initial_data = {}

    mood_metrics = {
        "Happiness": initial_data.get("Happiness", [])
        + [data.happiness_level for data in mood_data],
        "Stress": initial_data.get("Stress", [])
        + [data.stress_level for data in mood_data],
        "Relaxation": initial_data.get("Relaxation", [])
        + [data.relaxation_level for data in mood_data],
        "Energy": initial_data.get("Energy", [])
        + [data.energy_level for data in mood_data],
        "Creativity": initial_data.get("Creativity", [])
        + [data.creativity_level for data in mood_data],
        "Focus": initial_data.get("Focus", [])
        + [data.focus_level for data in mood_data],
        "Social": initial_data.get("Social", [])
        + [data.social_level for data in mood_data],
        "Motivation": initial_data.get("Motivation", [])
        + [data.motivation_level for data in mood_data],
        "Confidence": initial_data.get("Confidence", [])
        + [data.confidence_level for data in mood_data],
        "Contentment": initial_data.get("Contentment", [])
        + [data.contentment_level for data in mood_data],
    }

    colors = {
        "Happiness": "#4CAF50",  # Vibrant green
        "Stress": "#FF5252",  # Muted red
        "Relaxation": "#2196F3",  # Soothing blue
        "Energy": "#FFEB3B",  # Bright yellow
        "Creativity": "#9C27B0",  # Rich purple
        "Focus": "#00BCD4",  # Clean cyan
        "Social": "#FF9800",  # Defined orange
        "Motivation": "#E91E63",  # Lively pink
        "Confidence": "#FFC107",  # Nice amber
        "Contentment": "#009688",  # Teal (lol)
    }

    plot_divs = {}
    # Create plot for each metric
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
            ticktext=["Not at all", "Not really", "Neutral", "Somewhat", "Completely"],
        )

        fig.update_xaxes(type="category")

        plot_divs[metric] = opy.plot(fig, output_type="div", include_plotlyjs=False)

    context = {"plot_divs": plot_divs}

    return render(request, "moodtracker/mood_graph.html", context)
