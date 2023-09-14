from django.urls import path
from . import views

# Variable: app_name - The name of the app
app_name = "moodtracker"

# Variable: urlpatterns - The URL patterns for the app
urlpatterns = [
    path("", views.home, name="home"),
    path("questionnaire/", views.questionnaire_view, name="questionnaire"),
    path("save-mood/", views.save_mood, name="save_mood"),
    path("mood-graph/", views.mood_graph_view, name="mood_graph"),
]
