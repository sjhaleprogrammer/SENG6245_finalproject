from django.shortcuts import render
from .apps import WeatherConfig

def index(request):
    # Use the processed data in your view
    return render(request, 'index.html', {'processed_data': WeatherConfig.data})
