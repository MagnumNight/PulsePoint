from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.home, name='home'),
    path('create_forum/', views.create_forum, name='create_forum')
]