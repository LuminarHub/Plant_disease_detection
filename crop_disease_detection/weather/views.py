import requests
import os
from django.shortcuts import render
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

OPENWEATHER_API_KEY = r'47d77a0b00b65efb9dd99b32fd2295e3'

def weather_view(request):
    city = request.GET.get('city', '')
    weather_data = None
    error = None

    if city:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200 and "main" in data:
                weather_data = {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'description': data['weather'][0]['description'].title(),
                    'icon': data['weather'][0]['icon'],
                    'country': data['sys']['country']
                }
            else:
                error = f"City '{city}' not found. Please enter a valid city name."

        except Exception as e:
            print("Weather API Error:", e)
            error = "⚠️ Unable to fetch weather data right now."

    return render(request, 'weather/weather.html', {
        'weather_data': weather_data,
        'error': error,
        'city': city
    })
