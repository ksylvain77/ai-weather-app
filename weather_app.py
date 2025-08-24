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
from datetime import datetime, timedelta

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
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                color: #333;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .header {
                text-align: center;
                margin-bottom: 30px;
                color: white;
            }
            
            .header h1 {
                font-size: 2.5em;
                font-weight: 300;
                margin-bottom: 10px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            
            .location-info {
                font-size: 1.1em;
                opacity: 0.9;
            }
            
            .weather-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 30px;
            }
            
            @media (max-width: 768px) {
                .weather-grid {
                    grid-template-columns: 1fr;
                }
            }
            
            .current-weather {
                background: rgba(255,255,255,0.95);
                backdrop-filter: blur(10px);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                text-align: center;
                grid-column: 1 / -1;
            }
            
            .temp-display {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 20px;
                margin: 20px 0;
            }
            
            .main-temp { 
                font-size: 4em; 
                font-weight: 200; 
                color: #2d3436;
                line-height: 1;
            }
            
            .weather-icon {
                font-size: 3em;
            }
            
            .description { 
                font-size: 1.3em; 
                color: #636e72; 
                text-transform: capitalize;
                margin-bottom: 30px;
            }
            
            .weather-details { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                gap: 20px; 
                margin-top: 30px; 
            }
            
            .detail-card {
                background: rgba(116, 185, 255, 0.1);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                border: 1px solid rgba(255,255,255,0.2);
            }
            
            .detail-label {
                font-size: 0.9em;
                color: #74b9ff;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 8px;
            }
            
            .detail-value {
                font-size: 1.4em;
                font-weight: 500;
                color: #2d3436;
            }
            
            .forecast-section {
                background: rgba(255,255,255,0.95);
                backdrop-filter: blur(10px);
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            }
            
            .forecast-title { 
                font-size: 1.8em; 
                margin-bottom: 25px; 
                color: #2d3436;
                font-weight: 300;
                text-align: center;
            }
            
            .forecast-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 15px;
            }
            
            .forecast-day {
                text-align: center;
                padding: 20px 15px;
                background: rgba(116, 185, 255, 0.1);
                border-radius: 15px;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                border: 1px solid rgba(255,255,255,0.2);
            }
            
            .forecast-day:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            
            .day-name { 
                font-weight: 600; 
                margin-bottom: 10px;
                color: #74b9ff;
                font-size: 0.9em;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .day-temps { 
                font-size: 1.1em;
                margin: 10px 0;
                color: #2d3436;
            }
            
            .day-desc {
                font-size: 0.85em;
                color: #636e72;
                text-transform: capitalize;
                margin-top: 8px;
            }
            
            .rain-chance {
                font-size: 0.8em;
                color: #74b9ff;
                margin-top: 5px;
                font-weight: 500;
            }
            
            .footer {
                text-align: center;
                margin-top: 30px;
                color: rgba(255,255,255,0.8);
                font-size: 0.9em;
            }
            
            .update-time {
                background: rgba(255,255,255,0.1);
                padding: 10px 20px;
                border-radius: 25px;
                display: inline-block;
                backdrop-filter: blur(10px);
            }
            
            .error-message {
                background: rgba(255,255,255,0.95);
                backdrop-filter: blur(10px);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                text-align: center;
                margin: 20px 0;
            }
            
            .error-title {
                font-size: 1.5em;
                color: #e17055;
                margin-bottom: 15px;
            }
            
            .error-text {
                color: #636e72;
                line-height: 1.6;
            }
            
            .api-setup {
                background: rgba(116, 185, 255, 0.1);
                padding: 20px;
                border-radius: 15px;
                margin-top: 20px;
                border-left: 4px solid #74b9ff;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Personal Weather</h1>
                <div class="location-info">{{ current.location }}, {{ current.country }}</div>
            </div>
            
            <div class="current-weather">
                <div class="temp-display">
                    <div class="weather-icon">🌤️</div>
                    <div class="main-temp">{{ "%.0f"|format(current.temperature) }}°</div>
                </div>
                <div class="description">{{ current.description }}</div>
                
                <div class="weather-details">
                    <div class="detail-card">
                        <div class="detail-label">Feels Like</div>
                        <div class="detail-value">{{ "%.0f"|format(current.feels_like) }}°F</div>
                    </div>
                    <div class="detail-card">
                        <div class="detail-label">Humidity</div>
                        <div class="detail-value">{{ current.humidity }}%</div>
                    </div>
                    <div class="detail-card">
                        <div class="detail-label">Wind Speed</div>
                        <div class="detail-value">{{ "%.1f"|format(current.wind_speed) }} mph</div>
                    </div>
                    <div class="detail-card">
                        <div class="detail-label">Visibility</div>
                        <div class="detail-value">{{ "%.1f"|format(current.visibility) }} mi</div>
                    </div>
                    <div class="detail-card">
                        <div class="detail-label">Pressure</div>
                        <div class="detail-value">{{ current.pressure }} hPa</div>
                    </div>
                    <div class="detail-card">
                        <div class="detail-label">Sunrise</div>
                        <div class="detail-value">{{ current.sunrise.strftime('%H:%M') }}</div>
                    </div>
                </div>
            </div>
            
            {% if forecast.forecasts %}
            <div class="forecast-section">
                <div class="forecast-title">7-Day Forecast</div>
                <div class="forecast-grid">
                    {% for day in forecast.forecasts %}
                    <div class="forecast-day">
                        <div class="day-name">{{ day.date.strftime('%a') }}</div>
                        <div class="day-temps">
                            <strong>{{ "%.0f"|format(day.temp_high) }}°</strong> / {{ "%.0f"|format(day.temp_low) }}°
                        </div>
                        <div class="day-desc">{{ day.description|title }}</div>
                        {% if day.rain_chance > 0 %}
                        <div class="rain-chance">{{ "%.0f"|format(day.rain_chance) }}% rain</div>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
            
            <div class="footer">
                <div class="update-time">
                    Last updated: {{ current.timestamp.strftime('%H:%M') }}
                </div>
            </div>
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
