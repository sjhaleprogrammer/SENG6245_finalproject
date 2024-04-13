from django.http import HttpResponse
from weather.models import Weather
import requests
import json
from datetime import datetime
   
def home(request):
    return HttpResponse("Hello, welcome to the weather api backend") 



# this method gets the client ip address and uses that to get the weather data
# note this is not fully tested and may crash and work if apis being used go down.

def weatherapicall(request):
    # Fetching location data based on IP address
    ip_address = '75.110.12.97'  # For local testing, you may want to use a default IP address
    ip_data = requests.get(f"http://ip-api.com/json/{ip_address}").json()
    lat = ip_data.get('lat')
    lon = ip_data.get('lon')
    
    # Calling weather API
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m"
    }
    weather_response = requests.get(url, params=params)
    weatherdata = weather_response.json()
    
    # Extracting hourly temperature data
    hourly_weather_data = weatherdata.get('hourly')
    hourly_time_temp_dict = dict(zip(hourly_weather_data.get('time'), hourly_weather_data.get('temperature_2m')))
    
    # Storing temperature data in a single Weather object
    weather_date = datetime.now()  # You can use any suitable datetime
    weather_obj = Weather.create_weather(weather_date, hourly_time_temp_dict)
    weather_obj.save()
    
    # Return weather data as JSON response
    return HttpResponse(json.dumps(weatherdata, indent=4).encode('utf-8'), content_type='application/json')

# method to call chatapi api
def chatapicall(request):
    return


