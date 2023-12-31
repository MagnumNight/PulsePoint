from django import forms
from .models import Questionnaire, MoodData


# Class: QuestionnaireForm - Django form for questionnaire model
class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = [
            "happiness_level",
            "stress_level",
            "relaxation_level",
            "energy_level",
            "creativity_level",
            "focus_level",
            "social_level",
            "motivation_level",
            "confidence_level",
            "contentment_level",
        ]


# Class: MoodDataForm - Django form for mood data model
class MoodDataForm(forms.ModelForm):
    class Meta:
        model = MoodData
        fields = [
            "happiness_level",
            "stress_level",
            "relaxation_level",
            "energy_level",
            "creativity_level",
            "focus_level",
            "social_level",
            "motivation_level",
            "confidence_level",
            "contentment_level",
        ]
