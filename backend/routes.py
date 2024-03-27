from django.shortcuts import render        
from django.http import HttpResponse
import requests
   
def home(request):
    return HttpResponse("Hello, welcome to the weather api backend") 



# this method gets the client ip address and uses that to get the weather data
# note this is not fully tested and may crash and work if apis being used go down.

def weatherapicall(request): 
    # this gets the actual ip address but this will not do when ran locally
    #ip_address = request.META.get('REMOTE_ADDR') 
    
    ip_address = '75.110.12.97'

    ip_data = requests.get(f"http://ip-api.com/json/{ip_address}").json()

    lat = ip_data.get('lat')   
    lon = ip_data.get('lon')

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": {lat},
        "longitude": {lon},
        "hourly": "temperature_2m"
    }
    weatherdata = requests.get(url, params=params).text

       
    return HttpResponse(weatherdata)



# method to call chatapi api
def chatapicall(request):
    return


