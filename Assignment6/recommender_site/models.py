from django.db import models
import user_based_algo as cf




class UserId (models.Model):
    user_id = models.CharField(max_length=5, choices=cf.getIds())

