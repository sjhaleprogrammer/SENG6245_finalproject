from django.http import HttpResponse, JsonResponse
from .models import Weather
import requests
import json
from datetime import datetime, date
   
def home(request):
    return HttpResponse("Hello, welcome to the weather api backend") 

# Retrieve weather data for the current day
def get_temperature_data(request):
    
    today = date.today()

    weather_data = Weather.objects.filter(weather_date__date=today)

    serialized_data = [{'weather_date': item.weather_date, 'temperature_data': item.temperature_data} for item in weather_data]

    return JsonResponse(serialized_data, safe=False)


