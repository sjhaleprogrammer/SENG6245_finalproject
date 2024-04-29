from django.apps import AppConfig
import requests
import sys
from datetime import datetime




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
    
   pass 
   
      

def save_weather_data(hourly_time_temp_dict):
    from .models import Weather
    weather_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    weather_obj = Weather.objects.create(weather_date=weather_date, temperature_data=hourly_time_temp_dict)
    return weather_obj


def save_ai_summary(weather_obj, summary_text):
    from .models import AISummary
    ai_summary = AISummary.objects.create(weather=weather_obj, text=summary_text)
    return ai_summary

def retrieve_curret_data():
    from .models import Weather
    from datetime import datetime
    
    curr_date = datetime.now().date()
    start_date = datetime.combine(curr_date, datetime.min.time())
    end_date = datetime.combine(curr_date, datetime.max.time())
    
    data = Weather.objects.filter(weather_date__range=(start_date,end_date))
    
    return data

class WeatherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather'

    def ready(self):
        from .models import Weather
        from datetime import datetime
        
        if 'runserver' not in sys.argv:
            return

        try:
            data = retrieve_curret_data()
            if data is not None:
                print('data found and returned successfully')
                return data
            else:
                hourly_time_temp_dict = get_weather_data()
                weather_obj = save_weather_data(hourly_time_temp_dict)
                summary_text = call_ai_api(hourly_time_temp_dict)
                save_ai_summary(weather_obj, summary_text)
                print("Weather data and ChatGPT summary saved successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
