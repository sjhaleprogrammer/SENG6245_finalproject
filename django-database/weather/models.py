from django.db import models

class Weather(models.Model):
    weather_date = models.DateTimeField("date",primary_key=True)
    temp = models.FloatField("temp")
    
