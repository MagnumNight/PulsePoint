from django import forms
from .models import Forum
from .models import Post

# Class: ForumForm - Form for creating a new forum
class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ["title", "description"]

# Class: PostForm - Form for creating a new post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
