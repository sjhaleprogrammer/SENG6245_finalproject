from django.test import TestCase
from unittest.mock import patch
from datetime import datetime
from .models import AISummary, Weather

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

class TestAISummary(TestCase):

    @patch('openai.Completion.create')
    def test_generate_weather_summary(self, mock_completion_create):
    # Mock the OpenAI API response with correct structure
        mock_completion_create.return_value = {
        'choices': [{'text': 'Clear skies with mild temperatures.'}]
    }

    # Call the generate_weather_summary method with a string weather description
        weather_data = "Clear skies with mild temperatures."
        summary_text = AISummary.generate_weather_summary(weather_data)
        print("Response from generate_weather_summary:", summary_text)  # Add this line to print the summary text

    # Check if the summary text is correct
        self.assertEqual(summary_text, 'Clear skies with mild temperatures.')

    def test_save_summary_to_database(self):
        # Create a dummy Weather instance
        weather_instance = Weather.objects.create(weather_date=datetime.now(), temperature=20, condition='clear')

        # Call the save_summary_to_database method with a dummy weather summary
        summary_text = 'Clear skies with mild temperatures.'
        AISummary.save_summary_to_database(summary_text, weather_instance)

        # Check if the summary was saved in the database
        summary_instance = AISummary.objects.first()
        self.assertEqual(summary_instance.text, summary_text)
        self.assertEqual(summary_instance.weather, weather_instance)


class ConnectionErrorTests(TestCase):
    @patch('weather.apps.requests.get')
    def test_get_weather_data_connection_error(self, mock_requests_get):
        # Set up mock response object for connection error
        mock_requests_get.side_effect = ConnectionError()

        # Test if ConnectionError is raised when there's a connection issue
        with self.assertRaises(ConnectionError):
            get_weather_data()

    @patch('weather.apps.requests.get')
    def test_get_weather_data_invalid_response(self, mock_requests_get):
        # Set up mock response object for invalid response (missing data)
        mock_response = mock_requests_get.return_value
        mock_response.status_code = 200
        mock_response.json.side_effect = [{"lat": 40.7128}, None]  # Missing "lon" in first response, None in second

        # Test if ValueError is raised when data is incomplete
        with self.assertRaises(ValueError) as context:
            get_weather_data()

        # Assert the exception message
        self.assertEqual(str(context.exception), "Incomplete weather data received")


