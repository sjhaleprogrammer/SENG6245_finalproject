from django.apps import AppConfig
from django.utils import timezone
from datetime import datetime, date
import requests
import cohere
import sys



# resolve ip address to lat and lon
def call_ip_api(ip_address):

    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    if response.status_code == 200:
        ip_data = response.json()
        return ip_data.get('lat'), ip_data.get('lon')
    else:
        raise ValueError(f"Error fetching IP data: {response.status_code}, {response.text}")


# get weather data
def call_weather_api(lat, lon):

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


# get AI summary
def call_ai_api(weatherdata):
    
    prompt = f"Here are is hourly celsius temperatures {weatherdata}. Act like a news caster and generate a summary of the weather, this is going on the front of a website not too long"
    client = cohere.Client(api_key="fIUcvIBKj77qssfAOoJu1ZCnQjxSTtCK3BmrTDb0",)
    try:
        chat = client.chat(
            message=f"{prompt}",
            model="command"
        )
        return chat.text
    except Exception as e:
        print(f"An error occurred while calling AI: {e}")
        return None 
   
      
#save weather data
def save_weather_data(hourly_time_temp_dict):
    from .models import Weather
    weather_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    weather_obj = Weather.objects.create(weather_date=weather_date, temperature_data=hourly_time_temp_dict)
    return weather_obj

#save AI summary
def save_ai_summary(weather_obj, summary_text, curr_date):
    from .models import AISummary
    today = timezone.now().date()  # Get the current date without considering timezone
    ai_summary, created = AISummary.objects.get_or_create(weather=weather_obj, defaults={'text': summary_text, 'created_at': curr_date})
    if not created:
        ai_summary.text = summary_text
        ai_summary.created_at = curr_date
        ai_summary.save()
    return ai_summary




class WeatherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather'
    


    # note the implementation of ready() is not meant to be ran for production instead in a realworld app would us a cron job because the website would be always running.
    def ready(self):

        if not 'runserver' in sys.argv:
            return

        from .models import Weather, AISummary
        try:
          curr_date = timezone.now().date()
          print("Today's date:", curr_date)
          print("Checking if weather data and AI summary already exist...")

          today_weather = Weather.objects.filter(weather_date__day = datetime.now().day).first()
          today_ai_summary = AISummary.objects.filter(created_at= date.today()).first()

          if today_weather is None:
            print("Weather data not found. Fetching data...")
            lat, lon = call_ip_api('75.110.12.97')  
            hourly_time_temp_dict = call_weather_api(lat,lon)  
            save_weather_data(hourly_time_temp_dict)
            today_weather = Weather.objects.filter(weather_date__day = datetime.now().day).first()
          else:
            print("Weather data already exists for today.")

          if today_ai_summary is None:
             print("AI summary not found. Generating summary...") 
             ai_summary = call_ai_api(today_weather.temperature_data)
             if ai_summary is not None:
               save_ai_summary(today_weather, ai_summary, curr_date)
               print("Weather data and AI summary saved successfully.")
             else:
               data = "Failed to generate AI summary."
          else:
            print("AI summary already exists for today.")

        except Exception as e:
            print(f"An error occurred: {e}")
            data = "Error loading data"

    


        
