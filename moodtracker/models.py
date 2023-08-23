from django.db import models
from django.contrib.auth.models import User


class Questionnaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_color = models.CharField(max_length=100)
    mood_rating = models.IntegerField(choices=[(1, "Bad"), (2, "Okay"), (3, "Good")])


class MoodData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    mood_rating = models.IntegerField(choices=[(1, "Bad"), (2, "Okay"), (3, "Good")])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "date")
