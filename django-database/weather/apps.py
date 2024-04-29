from django.apps import AppConfig
from django.utils import timezone
from openai import OpenAI
import requests
import sys



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
    response.raise_for_status()  # Raises an HTTPError for bad status codes
    weatherdata = response.json()
    hourly_weather_data = weatherdata.get('hourly')
    hourly_time_temp_dict = hourly_weather_data.get('temperature_2m')
    return hourly_time_temp_dict


def call_ai_api(weatherdata):
    prompt = f"The weather outside is currently {weatherdata}. Can you provide a summary of what's going on?"
    client = OpenAI(api_key="needs a working API KEY")
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt}",
                }
            ],
            model="gpt-3.5-turbo",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred while calling OpenAI: {e}")
        return None


def save_weather_data(hourly_time_temp_dict):
    from .models import Weather
    weather_date = timezone.now().date()  # Get the current date without considering timezone
    weather_obj = Weather.objects.get_or_create(weather_date=weather_date, defaults={'temperature_data': hourly_time_temp_dict})
    return weather_obj


def save_ai_summary(weather_obj, summary_text):
    from .models import AISummary
    today = timezone.now().date()  # Get the current date without considering timezone
    ai_summary = AISummary.objects.get_or_create(weather__weather_date=today, defaults={'text': summary_text})
    return ai_summary


class WeatherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather'


    def ready(self):
        from .models import Weather, AISummary

        if 'runserver' not in sys.argv:
            return
        try:
            # Check if weather data for today already exists in the database
            today_weather = Weather.objects.filter(weather_date=timezone.now().date()).first()
                                   
            if today_weather:
                # Data for today already exists, no need to fetch and save again
                print("Weather data for today already exist.")
                print("Checking if AI summary for today already exists in the database...")
                if not AISummary.objects.filter(weather__weather_date=timezone.now().date()).exists():
                    # AI summary for today does not exist in the database
                    ai_summary = call_ai_api(today_weather.temperature_data)
                    if ai_summary is not None:
                        print(ai_summary)
                        save_ai_summary(today_weather, ai_summary)
                        print("Weather data and ChatGPT summary saved successfully.")
                    else:
                        print("Failed to generate AI summary.")
                else:
                    print("Weather data and AI summary already exist.")
            else:
                hourly_time_temp_dict = get_weather_data()
                weather_obj = save_weather_data(hourly_time_temp_dict)
                if weather_obj:
                    # AI summary for today does not exist in the database
                    ai_summary = call_ai_api(hourly_time_temp_dict)
                    if ai_summary is not None:
                        print(ai_summary)
                        save_ai_summary(weather_obj, ai_summary)
                        print("Weather data and ChatGPT summary saved successfully.")
                    else:
                        print("Failed to generate AI summary.")
                else:
                    print("Failed to save weather data.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching weather data: {e}")

 
        except Exception as e:
            print(f"An error occurred: {e}")


