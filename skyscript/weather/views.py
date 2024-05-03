from django.shortcuts import render
from datetime import date
from .models import AISummary
from .models import Weather
from datetime import datetime

def index(request):
    
    aisummary = AISummary.objects.filter(created_at= date.today() )

    weatherdata = Weather.objects.filter(weather_date__day = datetime.now().day)

    current_date = datetime.now().date()
    
    #avg temperature
    temperature = sum(weatherdata.values_list('temperature_data', flat=True)[0])/len(weatherdata.values_list('temperature_data', flat=True)[0])


    min_temperature = min(weatherdata.values_list('temperature_data', flat=True)[0])

    max_temperature = max(weatherdata.values_list('temperature_data', flat=True)[0])
    
    return render(request, 'index.html', {
        'processed_data': aisummary[0].text,
        'temperature': temperature.__round__(2),
        'current_date': current_date,
        'min_temperature': min_temperature.__round__(2),
        'max_temperature': max_temperature.__round__(2)
    })
    
    
