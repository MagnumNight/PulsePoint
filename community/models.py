from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Forum(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # Function: __str__ - Return the title of the forum
    def __str__(self):
        return self.title


# Compare this snippet from community/models.py:
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # Function: __str__ - Return the title of the post
    def __str__(self):
        return self.title
