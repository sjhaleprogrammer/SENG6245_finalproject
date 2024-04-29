from django.http import HttpResponse, JsonResponse
from .models import Weather
import requests
import json
from datetime import datetime, date
from .models import AISummary

   
def home(request):
    return HttpResponse("Hello, welcome to the weather api backend") 

# Retrieve weather data for the current day
def get_temperature_data(request):
    
    today = date.today()

    weather_data = Weather.objects.filter(weather_date__date=today)

    serialized_data = [{'weather_date': item.weather_date, 'temperature_data': item.temperature_data} for item in weather_data]

    return JsonResponse(serialized_data, safe=False)



def weather_detail(request, weather_id):
    # Retrieve weather data from database
    weather_instance = Weather.objects.get(pk=weather_id)

    # Generate summary
    weather_data = {"temperature": weather_instance.temperature, "humidity": weather_instance.humidity, "description": weather_instance.description}
    summary_text = AISummary.generate_weather_summary(weather_data)

    # Save summary to database
    AISummary.save_summary_to_database(summary_text, weather_instance)

