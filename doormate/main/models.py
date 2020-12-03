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


class Events(models.Model):
    summary = models.CharField(max_length=200,primary_key=True)
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=200)