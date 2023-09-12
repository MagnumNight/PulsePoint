from django.db import models
from django.contrib.auth.models import User

# Class: Questionnaire - Django model for questionnaire
class Questionnaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    happiness_level = models.IntegerField(default=3)
    stress_level = models.IntegerField(default=3)
    relaxation_level = models.IntegerField(default=3)
    energy_level = models.IntegerField(default=3)
    creativity_level = models.IntegerField(default=3)
    focus_level = models.IntegerField(default=3)
    social_level = models.IntegerField(default=3)
    motivation_level = models.IntegerField(default=3)
    confidence_level = models.IntegerField(default=3)
    contentment_level = models.IntegerField(default=3)

# Class: MoodData - Django model for mood data
class MoodData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    happiness_level = models.IntegerField(default=3)
    stress_level = models.IntegerField(default=3)
    relaxation_level = models.IntegerField(default=3)
    energy_level = models.IntegerField(default=3)
    creativity_level = models.IntegerField(default=3)
    focus_level = models.IntegerField(default=3)
    social_level = models.IntegerField(default=3)
    motivation_level = models.IntegerField(default=3)
    confidence_level = models.IntegerField(default=3)
    contentment_level = models.IntegerField(default=3)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "date")
