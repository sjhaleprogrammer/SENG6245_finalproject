from django.test import TestCase
from unittest.mock import patch
from apps import *  

class Tests(TestCase):
    @patch('weather.apps.requests.get')
    def test_get_weather_data_success(self, mock_requests_get):
        # Mock IP data response
        mock_ip_data = {
            "lat": 40.7128,
            "lon": -74.0060
        }

        # Mock weather data response
        mock_weather_data = {
            "hourly": {
                "temperature_2m": {
                    "2024-04-28T00:00:00": 20.1,
                    "2024-04-28T01:00:00": 19.5,
                    "2024-04-28T02:00:00": 18.9,
                }
            }
        }

        # Set up mock response object
        mock_response = mock_requests_get.return_value
        mock_response.status_code = 200
        mock_response.json.side_effect = [mock_ip_data, mock_weather_data]

        # Call the function
        hourly_time_temp_dict = get_weather_data()

        # Assertions
        self.assertEqual(hourly_time_temp_dict, mock_weather_data['hourly']['temperature_2m'])

    @patch('weather.apps.requests.get')
    def test_get_weather_data_failure(self, mock_requests_get):
        # Set up mock response object for failure
        mock_response = mock_requests_get.return_value
        mock_response.status_code = 404
        mock_response.text = "Not Found"

        # Test if ValueError is raised
        with self.assertRaises(ValueError) as context:
            get_weather_data()

        # Assert the exception message
        self.assertEqual(str(context.exception), "Error fetching weather data: 404, Not Found")

