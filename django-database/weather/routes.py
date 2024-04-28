from django.http import HttpResponse
from django.http import JsonResponse
from .models import Weather
import requests
import json

   
def home(request):
    return HttpResponse("Hello, welcome to the weather api backend") 


def get_data(request):
    
    weather_data = Weather.objects.all()
  
    serialized_data = [{'weather_date': item.weather_date, 'temperature_data': item.temperature_data} for item in weather_data]
    
    return JsonResponse(serialized_data, safe=False)

# this method gets the client ip address and uses that to get the weather data
# note this is not fully tested and may crash and work if apis being used go down.

