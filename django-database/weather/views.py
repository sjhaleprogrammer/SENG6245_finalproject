from django.shortcuts import render
from django.utils import timezone
from .apps import WeatherConfig
from datetime import datetime
import requests
import cohere
from .models import Weather,AISummary

def get_weather_data():
    ip_address = '75.110.12.97'  
    ip_data = requests.get(f"http://ip-api.com/json/{ip_address}").json()
    lat = ip_data.get('lat')
    lon = ip_data.get('lon')

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        weatherdata = response.json()
        hourly_weather_data = weatherdata.get('hourly')
        hourly_time_temp_dict = hourly_weather_data.get('temperature_2m')
        return hourly_time_temp_dict
    else:
        raise ValueError(f"Error fetching weather data: {response.status_code}, {response.text}")


def call_ai_api(weatherdata):
    
    prompt = f"The weather outside is currently {weatherdata}. Can you provide a summary of what's going on?"
    client = cohere.Client(api_key="your key here",)
    try:
        chat = client.chat(
            message=f"{prompt}",
            model="command"
        )
        return chat
    except Exception as e:
        print(f"An error occurred while calling AI: {e}")
        return None 
   
      

def save_weather_data(hourly_time_temp_dict):
    weather_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    weather_obj = Weather.objects.create(weather_date=weather_date, temperature_data=hourly_time_temp_dict)
    return weather_obj


def save_ai_summary(weather_obj, summary_text):
    from .models import AISummary
    today = timezone.now().date()  # Get the current date without considering timezone
    ai_summary, created = AISummary.objects.get_or_create(weather=weather_obj, defaults={'text': summary_text})
    if not created:
        ai_summary.text = summary_text
        ai_summary.save()
    return ai_summary

def retrieve_current_data():
    curr_date = datetime.now().date()
    start_date = datetime.combine(curr_date, datetime.min.time())
    end_date = datetime.combine(curr_date, datetime.max.time())
    
    data = Weather.objects.filter(weather_date__range=(start_date,end_date))
    
    return data

def index(request):
    # Use the processed data in your view
    try:
        data = retrieve_current_data()
        
        if data is None:
            hourly_time_temp_dict = get_weather_data()
            weather_obj = save_weather_data(hourly_time_temp_dict)
            summary_text = call_ai_api(hourly_time_temp_dict)
            save_ai_summary(weather_obj, summary_text)
            print("Weather data and ChatGPT summary saved successfully.")
            data = retrieve_current_data()
    except Exception as e:
        print(f"An error occurred: {e}")
        data = "Error loading data"
    
    return render(request, 'index.html', {'processed_data': data})
