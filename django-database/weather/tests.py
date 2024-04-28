from django.test import TestCase, RequestFactory
from django.http import HttpRequest
from myapp.views import home, get_data, save_weather_data, save_ai_summary
from myapp.models import Weather, AISummary
import unittest
from unittest.mock import patch
from myapp import get_weather_data
from datetime import datetime

class HomeViewTestCase(TestCase):
    def test_home_function(self):
        request = HttpRequest()
        response = home(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Hello, welcome to the weather api backend")


class GetDataViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        # Create some sample weather data for testing
        Weather.objects.create(weather_date='2024-04-28', temperature_data=25.5)
        Weather.objects.create(weather_date='2024-04-29', temperature_data=26.5)

    def test_get_data_function(self):
        request = self.factory.get('/get_data/')
        response = get_data(request)
        self.assertEqual(response.status_code, 200)
        expected_response_data = [
            {'weather_date': '2024-04-28', 'temperature_data': 25.5},
            {'weather_date': '2024-04-29', 'temperature_data': 26.5}
        ]
        self.assertJSONEqual(str(response.content, encoding='utf-8'), expected_response_data)


class TestGetWeatherData(unittest.TestCase):
    @patch('myapp.requests.get')
    def test_get_weather_data_success(self, mock_requests_get):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "hourly": {
                "temperature_2m": {"time1": 20, "time2": 25}
            }
        }
        mock_requests_get.return_value = mock_response

        hourly_time_temp_dict = get_weather_data()
        self.assertIsNotNone(hourly_time_temp_dict)

    @patch('myapp.requests.get')
    def test_get_weather_data_failure(self, mock_requests_get):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_requests_get.return_value = mock_response

        with self.assertRaises(ValueError):
            get_weather_data()


class TestSaveWeatherData(TestCase):
    def test_save_weather_data(self):
        hourly_time_temp_dict = {"time1": 20, "time2": 25}
        weather_obj = save_weather_data(hourly_time_temp_dict)
        self.assertIsInstance(weather_obj, Weather)
        self.assertIsNotNone(weather_obj.weather_date)
        self.assertEqual(weather_obj.temperature_data, hourly_time_temp_dict)


class TestSaveAISummary(TestCase):
    def test_save_ai_summary(self):
        weather_obj = Weather.objects.create(weather_date=datetime.now(), temperature_data={"time1": 20, "time2": 25})
        summary_text = "This is a summary text."
        ai_summary = save_ai_summary(weather_obj, summary_text)
        self.assertIsInstance(ai_summary, AISummary)
        self.assertEqual(ai_summary.weather, weather_obj)
        self.assertEqual(ai_summary.text, summary_text)

