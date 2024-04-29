# SkyScript

## Overview
This project aims to create a dynamic weather forecast display website that provides users with accurate weather information based on their location. It utilizes data from the OpenWeather API to showcase temperature, humidity, wind speeds, precipitation, and weather conditions for different times of the day. The website features a user-friendly interface with dynamic elements that adjust based on real-time weather updates.

## Features
- Showcase temperature, humidity, wind speeds, precipitation, and weather conditions.
- Display weather forecasts for different points during the day.
- Dynamic user interface that adjusts based on real-time weather data.
- Collect user location preferences and store them in a SQLite database.
- Utilize API calls for data retrieval and updates from the OpenWeather API.
- Integration with OpenAI for generating smart and intuitive weather descriptions.
- Provide recommendations for appropriate clothing based on weather forecasts.

## Future Enhancements
- Implement a user login system for personalized experiences and data management.
- Introduce daily rewards to encourage user engagement.
- Provide historical weather data through graphical representations for analysis.

## Technologies Used
- Frontend: Astro for creating dynamic and efficient UI.
- Backend: Django framework for robust server-side functionality.
- Database: SQLite for storing user data and weather information.
- Integration: OpenAI for generating weather descriptions.

## Setup Instructions
1. Clone the repository.
2. Install the necessary dependencies using `pip install -r requirements.txt`.
3. Run migrations to set up the database schema: `python manage.py migrate`.
4. Start the Django development server: `python manage.py runserver`.
5. Access the website in your browser at `http://localhost:8000`.

## Data Source and Cleaning
- Retrieve weather data from the OpenWeather API, ensuring minute-by-minute forecasts.
- Clean and organize the retrieved data for efficient utilization in the application.


