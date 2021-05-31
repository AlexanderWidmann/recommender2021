from django.db import models


# Create your models here.

class MovieName(models.Model):
    movie_name = models.CharField(max_length=50)
