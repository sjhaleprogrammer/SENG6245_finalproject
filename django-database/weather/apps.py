from django.apps import AppConfig
from django.utils import timezone
import cohere
import requests
import sys

class WeatherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather'

    
