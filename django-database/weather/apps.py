from django.apps import AppConfig
import requests

class WeatherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather'

   
    def ready(self):
       prompt = "Once upon a time"
       url = "https://api.openai.com/v1/completions"
       headers = {
           "Authorization": "Bearer OPENAI_API_KEY",
           "Content-Type": "application/json"
       }
       data = {
            "model": "text-davinci-002",  # You can change the model if needed
            "prompt": prompt,
            "max_tokens": 100
       }
        
       response = requests.post(url, headers=headers, json=data)
        
       if response.status_code == 200:
         return response.json()["choices"][0]["text"]
       else:
        print("Error:", response.text)
        return None


