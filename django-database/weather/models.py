from django.db import models

class Weather(models.Model):
    weather_date = models.DateTimeField("date", primary_key=True)
    temperature_data = models.JSONField("temperature_data")

    def __str__(self):
        return f"Weather at {self.weather_date}: {self.temperature_data}"

    @classmethod
    def create_weather(cls, weather_date, temperature_data):
        return cls(weather_date=weather_date, temperature_data=temperature_data)



class AISummary(models.Model):
    weather = models.OneToOneField(Weather, on_delete=models.CASCADE, related_name='summary')
    created_at = models.DateTimeField("created_at")
    text = models.TextField()

    def __str__(self):
        return f"ChatGPT Summary for {self.weather.weather_date} ({self.created_at}) {self.text}"  

    

