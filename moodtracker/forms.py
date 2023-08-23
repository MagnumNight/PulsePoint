from django import forms
from .models import Questionnaire, MoodData


class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ["favorite_color", "mood_rating"]


class MoodDataForm(forms.ModelForm):
    class Meta:
        model = MoodData
        fields = ['mood_rating']
