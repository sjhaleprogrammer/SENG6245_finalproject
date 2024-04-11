from django.db import models

class Weather(models.Model):
    weather_date = models.DateTimeField("date")
    temp = models.FloatField("temp")
    