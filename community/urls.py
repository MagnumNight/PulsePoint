from django.urls import path
from . import views

# Variable: app_name - The name of the app
app_name = "community"

# Variable: urlpatterns - The URL patterns for the app
urlpatterns = [
    path("", views.home, name="home"),
    path("create_forum/", views.create_forum, name="create_forum"),
    path(
        "forum/<int:forum_id>/", views.forum_detail, name="forum_detail"
    ),
]
