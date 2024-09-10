from django.db import models

class Vote(models.Model):
    option = models.CharField(max_length=255)
    voter = models.CharField(max_length=255)