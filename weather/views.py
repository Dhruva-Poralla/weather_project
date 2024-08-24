from django.shortcuts import render
import requests
from .models import City, WeatherLog
from django.conf import settings
from .forms import CityForm
from rest_framework.response import Response
from rest_framework import status

def get_weather(request):
    city_name = 'New York'
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['city_name']
    else:
        form = CityForm()

    city, created = City.objects.get_or_create(name=city_name)
    api_key = settings.API_KEY
    api_url = settings.API_URL
    params = {
            "q": city_name,
            "appid": api_key,
            "units": "metric"    
    }
    
    response = requests.get(api_url, params=params)
    weather_data = response.json()
    if not weather_data.get('cod') == 200:
        context = {"error_message":"Failed to fetch weather data. Please try again later."}
        return render(request, 'weather_report.html', context)
    
    temperature = weather_data.get('main', {}).get('temp')
    humidity = weather_data.get('main', {}).get('humidity')
    description = weather_data.get('weather', [{}])[0].get('description')
    icon = weather_data.get('weather', [{}])[0].get('icon')
    wind_speed = weather_data.get('wind', {}).get('speed') # by default speed is miles per seconds
    
    # Check for extreme weather conditions
    alert_messages = {}
    if temperature:
        if temperature > 40:
            alert_messages['High Temperature Alert'] = f"Extreme Heat Alert: {temperature}°C! Stay indoors and keep hydrated."
        elif temperature < 0:
            alert_messages['Low Temperature Alert'] = f"Extreme Cold Alert: {temperature}°C! Dress warmly and stay safe."
            

    if "storm" in description.lower() or "hurricane" in description.lower() or "tornado" in description.lower():
        alert_messages['Bad Weather Alert'] = f"Severe Weather Alert: {description.capitalize()}! Take necessary precautions."
        
    if wind_speed and wind_speed >= 12:
        alert_messages['Bad Weather Alert'] = f"Strong Breeze Alert: Don't go out stay inside."
        


    WeatherLog.objects.create(
        city=city,
        temperature=temperature,
        humidity = humidity,
        description=description,
        icon=icon,
        response = weather_data
    )
    

    context = {
        'city': city_name,
        'temperature': temperature,
        'humidity':humidity,
        'description': description,
        'icon': icon,
        'form': form,
    }
    
    if alert_messages:
        context['alert_messages'] = alert_messages.values()

    return render(request, 'weather_report.html', context)
    
    