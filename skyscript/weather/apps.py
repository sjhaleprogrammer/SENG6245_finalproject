from django.apps import AppConfig
from django.utils import timezone
from datetime import datetime, date
import requests
import cohere
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

def save_weather_data(hourly_time_temp_dict):
    from .models import Weather
    weather_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    weather_obj = Weather.objects.create(weather_date=weather_date, temperature_data=hourly_time_temp_dict)
    return weather_obj


def save_ai_summary(weather_obj, summary_text, curr_date):
    ai_summary, _ = AISummary.objects.get_or_create(
        weather=weather_obj,
        defaults={'text': summary_text, 'created_at': curr_date}
    )

    # Update text and created_at if the AISummary object already exists
    ai_summary.text = summary_text
    ai_summary.created_at = curr_date
    ai_summary.save()

    return ai_summary

def retrieve_current_data():
    curr_date = datetime.now().date()
    start_date = datetime.combine(curr_date, datetime.min.time())
    end_date = datetime.combine(curr_date, datetime.max.time())
    
    data = Weather.objects.filter(weather_date__range=(start_date,end_date))
    
    return data

class WeatherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather'

    def ready(self):
        from .models import Weather, AISummary
        try:
            curr_date = timezone.now().date()
            print('current date:::: ', curr_date)

            # Fetch weather today
            today_weather = Weather.objects.filter(weather_date__day=datetime.now().day).first()

            if today_weather is None:
                hourly_time_temp_dict = get_weather_data()
                save_weather_data(hourly_time_temp_dict)
                today_weather = Weather.objects.filter(weather_date__day=datetime.now().day).first()

            if not AISummary.objects.filter(created_at=curr_date).exists():
                ai_summary = call_ai_api(today_weather.temperature_data)
                if ai_summary is not None:
                    save_ai_summary(today_weather, ai_summary, curr_date)
                    print("Weather data and AI summary saved successfully.")
                else:
                    print("Failed to generate AI summary.")
            else:
                print("AI summary already exists for today.")

        except Exception as e:
            print(f"An error occurred: {e}")
            print("Error loading data")

    


        
