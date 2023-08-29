from django.db import models
from django.contrib.auth.models import User

MOOD_CHOICES = [
    ("ecstatic", "🤩 Ecstatic"),
    ("happy", "😁 Happy"),
    ("neutral", "😐 Neutral"),
    ("confused", "😕 Confused"),
    ("worried", "😟 Worried"),
    ("sad", "😢 Sad"),
    ("crying", "😭 Crying"),
    ("disappointed", "😞 Disappointed"),
    ("angry", "😡 Angry"),
    ("frustrated", "😤 Frustrated"),
    ("confident", "😎 Confident"),
    ("annoyed", "😖 Annoyed"),
    ("stressed", "😓 Stressed"),
    ("relieved", "😌 Relieved"),
    ("thinking", "🤔 Thinking"),
]


class Questionnaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_color = models.CharField(max_length=100)
    mood_rating = models.CharField(max_length=20, choices=MOOD_CHOICES)


class MoodData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    mood_rating = models.CharField(max_length=20, choices=MOOD_CHOICES)
    mood_emoji = models.CharField(max_length=5, default="🙂")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "date")
