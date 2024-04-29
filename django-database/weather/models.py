from django.db import models
import openai

class Weather(models.Model):
    weather_date = models.DateTimeField("date", primary_key=True)
    temperature_data = models.JSONField("temperature_data")

    def __str__(self):
        return f"Weather at {self.weather_date}: {self.temperature_data}"

    @classmethod
    def create_weather(cls, weather_date, temperature_data):
        return cls(weather_date=weather_date, temperature_data=temperature_data)



class AISummary(models.Model):
    weather = models.OneToOneField(Weather, on_delete=models.CASCADE, related_name='summary')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return f"ChatGPT Summary for {self.weather.weather_date} ({self.created_at})"
    

    @staticmethod
    def generate_weather_summary(weatherdata):
        prompt = f"The weather outside is currently {weatherdata}. Can you provide a summary of what's going on?"
        openai.api_key = 'sk-proj-4rNF89GeBsAQ3PEbrEdyT3BlbkFJQZhuk8o5fa8eWuUpChWY'
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=40
        )
    # Ensure the response is not None
        if response is not None and 'choices' in response and response['choices']:
            summary_text = response['choices'][0]['text'].strip()
            return summary_text
        else:
        # If the response is None or empty, return an error message or handle it appropriately
            return "Error: Unable to generate weather summary"
    @staticmethod
    def save_summary_to_database(weather_summary, weather_instance):
        summary_instance = AISummary.objects.create(weather=weather_instance, text=weather_summary)
        summary_instance.save()


