from django import forms
from .models import Forum

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['title', 'description', 'date_created']
