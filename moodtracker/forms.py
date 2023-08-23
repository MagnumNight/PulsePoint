from django import forms
from .models import Questionnaire


class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ["favorite_color", "mood_rating"]
