from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from routes import weatherapicall
from unittest.mock import patch
import json

class WeatherapicallTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_weatherapicall(self):
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


