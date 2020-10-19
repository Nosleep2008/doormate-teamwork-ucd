from django.db import models

# Create your models here.

class AuthInfo(models.Model):
    email = models.EmailField()
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    token_type = models.CharField(max_length=100)

class Calendars(models.Model):
    calendar_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
