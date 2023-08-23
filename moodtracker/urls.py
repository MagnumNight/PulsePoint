from django.urls import path
from . import views

app_name = "moodtracker"

urlpatterns = [
    path("", views.home, name="home"),
    path("questionnaire/", views.questionnaire_view, name="questionnaire"),
    path("save-mood/", views.save_mood, name="save_mood"),
]
