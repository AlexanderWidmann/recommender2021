from django.db import models

# Create your models here.
class MovieId(models.Model):
    movieId = models.IntegerField(max_length=10)
    title = models.CharField(max_length=300)
