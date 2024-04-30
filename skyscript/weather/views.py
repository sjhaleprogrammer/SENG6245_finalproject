from django.shortcuts import render
from datetime import date
from .models import AISummary
from .apps import get_weather_data
from datetime import datetime

def index(request):
    
    data = AISummary.objects.filter(created_at= date.today() )

    temperature = get_weather_data()

    current_date = datetime.now().date()

    min_temperature = min(temperature)

    max_temperature = max(temperature)
    
    return render(request, 'index.html', {
        'processed_data': data[0].text,
        'temperature': temperature[0],
        'current_date': current_date,
        'min_temperature': min_temperature,
        'max_temperature': max_temperature
    })
    
    