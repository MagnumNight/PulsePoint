# Last Modified: 09/05/2023
# Modified by: Andrew Roney


from django.db import models

# Create your models here.
class Forum(models.Model):
    title: models.CharField(max_length=100)
    description: models.TextField()
    date_created: models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title