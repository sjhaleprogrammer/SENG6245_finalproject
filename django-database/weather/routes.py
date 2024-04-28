from django.http import HttpResponse
import requests
import json

   
def home(request):
    return HttpResponse("Hello, welcome to the weather api backend") 



# this method gets the client ip address and uses that to get the weather data
# note this is not fully tested and may crash and work if apis being used go down.

