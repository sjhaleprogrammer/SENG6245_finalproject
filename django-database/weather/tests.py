from django.test import TestCase, RequestFactory
from django.http import HttpResponse, JsonResponse
from .routes import weatherapicall, chatapicall, get_data, save_weather_data, save_ai_summary
from .models import Weather, AISummary
from .apps import WeatherConfig
from unittest.mock import patch
from datetime import datetime

class WeatherapicallTestCase(TestCase):
    """Test case for weatherapicall function"""

    def setUp(self):
        """Set up test environment"""
        self.factory = RequestFactory()

    def test_weatherapicall(self):
        """Test weatherapicall function"""
        # Mock the response from ip-api.com
        mock_ip_data = {
            'lat': 40.7128,
            'lon': -74.0060
        }

        # Mock the response from api.open-meteo.com
        mock_weather_data = {
            'hourly': {
                'time': ['2023-06-01T00:00', '2023-06-01T01:00'],
                'temperature_2m': [20.5, 19.8]
            }
        }

        # Create a mock request object
        request = self.factory.get('/weatherapicall/')

        # Patch the requests.get function to return the mock data
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = mock_ip_data
            mock_get.return_value.text = json.dumps(mock_weather_data)

            # Call the weatherapicall function
            response = weatherapicall(request)

        # Assert the response
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, json.dumps(mock_weather_data, indent=4).encode('utf-8'))
    
    def test_get_data(self):
        """Test get_data function"""
        # Create a mock request object
        request = self.client.get('/get-data/')

        # Patch the Weather model's objects.all() method to return mock data
        with patch('your_app.models.Weather.objects.all') as mock_all:
            # Mock weather data
            mock_weather_data = [
                {'weather_date': '2023-06-01T00:00', 'temperature_data': {'temperature': 20.5}},
                {'weather_date': '2023-06-01T01:00', 'temperature_data': {'temperature': 19.8}}
            ]
            mock_all.return_value = mock_weather_data

            # Call the get_data function
            response = get_data(request)

        # Assert the response
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, json.dumps(mock_weather_data, indent=4).encode('utf-8'))


class SaveWeatherAndSummaryTestCase(TestCase):
    """Test case for save_weather_data and save_ai_summary functions"""

    def setUp(self):
        """Set up test environment"""
        self.hourly_time_temp_dict = {
            '2023-06-01T00:00': 20.5,
            '2023-06-01T01:00': 19.8
        }
        self.summary_text = "Sample summary text."

    @patch('weather.routes.save_weather_data')
    @patch('weather.routes.save_ai_summary')
    def test_save_weather_and_summary(self, mock_save_weather_data, mock_save_ai_summary):
        """Test save_weather_data and save_ai_summary functions"""
        # Mock the save_weather_data function
        weather_obj = Weather.objects.create(weather_date=datetime.now(), temperature_data=self.hourly_time_temp_dict)
        mock_save_weather_data.return_value = weather_obj

        # Mock the save_ai_summary function
        ai_summary_obj = AISummary.objects.create(weather=weather_obj, text=self.summary_text)
        mock_save_ai_summary.return_value = ai_summary_obj

        # Call the save_weather_data and save_ai_summary functions
        saved_weather_obj = save_weather_data(self.hourly_time_temp_dict)
        saved_summary_obj = save_ai_summary(saved_weather_obj, self.summary_text)

        # Assert the return values
        self.assertEqual(saved_weather_obj, weather_obj)
        self.assertEqual(saved_summary_obj, ai_summary_obj)


class ChatapicallTestCase(TestCase):
    """Test case for chatapicall function"""

    def setUp(self):
        """Set up test environment"""
        self.factory = RequestFactory()

    def test_chatapicall(self):
        """Test chatapicall function"""
        # Create a mock request object
        request = self.factory.get('/chatgpt/')
        
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = {}
            response = chatapicall(request)
        
        # Assert the response
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
