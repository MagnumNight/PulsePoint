from django import forms
from .models import Questionnaire, MoodData


class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ["mood_rating"]


class MoodDataForm(forms.ModelForm):
    class Meta:
        model = MoodData
        fields = ["mood_rating"]