#!/usr/bin/env python3
"""
Weather app
a flask weather app

Entry point for the Weather app application.
"""

from flask import Flask, jsonify, request, render_template_string
import os
import sys
from pathlib import Path

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, that's ok

# Add modules directory to path
sys.path.insert(0, str(Path(__file__).parent / "modules"))

# Import your modules here
from core import get_status
from utils import get_timestamp
from weather_api import WeatherAPI, get_user_location

app = Flask(__name__)

# Initialize weather API
weather_api = WeatherAPI()

@app.route('/')
def home():
    """Main weather dashboard"""
    # Get user location
    location = get_user_location()
    
    if "error" in location:
        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Weather App</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>Weather App</h1>
            <p>Unable to detect location: {{ error }}</p>
            <p><a href="/weather/demo">View Demo Weather</a></p>
        </body>
        </html>
        """, error=location.get("error", "Unknown error"))
    
    # Get current weather and forecast
    current = weather_api.get_current_weather(location["latitude"], location["longitude"])
    forecast = weather_api.get_forecast(location["latitude"], location["longitude"])
    
    if "error" in current:
        return render_template_string("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Weather App</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>Weather App</h1>
            <p>Weather data unavailable: {{ error }}</p>
            <p>Make sure you have set OPENWEATHER_API_KEY in your environment.</p>
            <p>Get a free API key at: <a href="https://openweathermap.org/api">OpenWeatherMap</a></p>
        </body>
        </html>
        """, error=current.get("error", "Unknown error"))
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Weather App - {{ location.city }}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                max-width: 800px; 
                margin: 0 auto; 
                padding: 20px;
                background: linear-gradient(135deg, #74b9ff, #0984e3);
                min-height: 100vh;
            }
            .current-weather {
                background: rgba(255,255,255,0.9);
                padding: 30px;
                border-radius: 15px;
                margin-bottom: 20px;
                text-align: center;
            }
            .temp { font-size: 3em; font-weight: bold; color: #2d3436; }
            .location { font-size: 1.5em; color: #636e72; margin-bottom: 10px; }
            .description { font-size: 1.2em; color: #636e72; text-transform: capitalize; }
            .details { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
                gap: 15px; 
                margin-top: 20px; 
            }
            .detail-item { text-align: center; }
            .forecast {
                background: rgba(255,255,255,0.9);
                padding: 20px;
                border-radius: 15px;
            }
            .forecast-title { font-size: 1.5em; margin-bottom: 15px; color: #2d3436; }
            .forecast-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
                gap: 10px;
            }
            .forecast-day {
                text-align: center;
                padding: 10px;
                background: rgba(116, 185, 255, 0.1);
                border-radius: 8px;
            }
            .day-name { font-weight: bold; margin-bottom: 5px; }
            .day-temps { font-size: 0.9em; }
        </style>
    </head>
    <body>
        <div class="current-weather">
            <div class="location">{{ current.location }}, {{ current.country }}</div>
            <div class="temp">{{ "%.0f"|format(current.temperature) }}°C</div>
            <div class="description">{{ current.description }}</div>
            <div class="details">
                <div class="detail-item">
                    <strong>Feels like</strong><br>
                    {{ "%.0f"|format(current.feels_like) }}°C
                </div>
                <div class="detail-item">
                    <strong>Humidity</strong><br>
                    {{ current.humidity }}%
                </div>
                <div class="detail-item">
                    <strong>Wind</strong><br>
                    {{ "%.1f"|format(current.wind_speed) }} m/s
                </div>
                <div class="detail-item">
                    <strong>Visibility</strong><br>
                    {{ "%.1f"|format(current.visibility) }} km
                </div>
            </div>
        </div>
        
        {% if forecast.forecasts %}
        <div class="forecast">
            <div class="forecast-title">7-Day Forecast</div>
            <div class="forecast-grid">
                {% for day in forecast.forecasts %}
                <div class="forecast-day">
                    <div class="day-name">{{ day.date.strftime('%a') }}</div>
                    <div class="day-temps">
                        {{ "%.0f"|format(day.temp_high) }}° / {{ "%.0f"|format(day.temp_low) }}°
                    </div>
                    <div style="font-size: 0.8em; margin-top: 5px;">
                        {{ day.description|title }}
                    </div>
                    {% if day.rain_chance > 0 %}
                    <div style="font-size: 0.8em; color: #74b9ff;">
                        {{ "%.0f"|format(day.rain_chance) }}% rain
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
        
        <div style="text-align: center; margin-top: 20px; color: rgba(255,255,255,0.8);">
            <small>Last updated: {{ current.timestamp.strftime('%H:%M') }}</small>
        </div>
    </body>
    </html>
    """, current=current, forecast=forecast, location=location)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "weather_app",
        "timestamp": get_timestamp()
    })

@app.route('/api/weather')
def api_weather():
    """API endpoint for current weather"""
    location = get_user_location()
    if "error" in location:
        return jsonify({"error": location["error"]}), 400
    
    weather = weather_api.get_current_weather(location["latitude"], location["longitude"])
    return jsonify(weather)

@app.route('/api/forecast')
def api_forecast():
    """API endpoint for weather forecast"""
    location = get_user_location()
    if "error" in location:
        return jsonify({"error": location["error"]}), 400
    
    forecast = weather_api.get_forecast(location["latitude"], location["longitude"])
    return jsonify(forecast)

@app.route('/api/location')
def api_location():
    """API endpoint for detected location"""
    location = get_user_location()
    return jsonify(location)

@app.route('/weather/demo')
def weather_demo():
    """Demo weather page with fixed coordinates"""
    # Montreal coordinates for demo
    demo_lat, demo_lon = 45.5017, -73.5673
    
    current = weather_api.get_current_weather(demo_lat, demo_lon)
    forecast = weather_api.get_forecast(demo_lat, demo_lon)
    
    if "error" in current:
        return f"Demo weather unavailable: {current.get('error')}"
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head><title>Weather Demo</title></head>
    <body>
        <h1>Demo Weather (Montreal)</h1>
        <h2>Current: {{ current.temperature }}°C - {{ current.description }}</h2>
        <p>Feels like: {{ current.feels_like }}°C | Humidity: {{ current.humidity }}%</p>
        <h3>7-Day Forecast:</h3>
        <ul>
        {% for day in forecast.forecasts[:7] %}
            <li>{{ day.date }}: {{ day.temp_high }}°/{{ day.temp_low }}° - {{ day.description }}</li>
        {% endfor %}
        </ul>
        <p><a href="/">← Back to Auto-Location Weather</a></p>
    </body>
    </html>
    """, current=current, forecast=forecast)

@app.route('/api')
def api_docs():
    """API documentation endpoint"""
    return jsonify({
        "name": "Weather App API",
        "version": "0.1.0",
        "description": "Personal weather app with auto-location and forecasts",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Main weather dashboard"},
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/api", "method": "GET", "description": "API documentation"},
            {"path": "/api/weather", "method": "GET", "description": "Current weather data"},
            {"path": "/api/forecast", "method": "GET", "description": "7-day weather forecast"},
            {"path": "/api/location", "method": "GET", "description": "Detected user location"},
            {"path": "/weather/demo", "method": "GET", "description": "Demo weather page"}
        ]
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting Weather app on port {port}")
    print(f"🌐 Server: http://localhost:5000")
    print(f"🔍 Health check: http://localhost:5000/health")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
