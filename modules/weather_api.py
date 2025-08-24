#!/usr/bin/env python3
"""
Weather API module for OpenWeatherMap integration

Handles weather data retrieval for the weather app.
"""

import requests
import os
from typing import Dict, Any, Optional
from datetime import datetime

class WeatherAPI:
    """
    OpenWeatherMap API client for weather data retrieval
    
    Free tier provides:
    - Current weather data
    - 5-day/3-hour forecast 
    - 1000 calls/day limit
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
    def get_current_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Get current weather for given coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dict containing current weather data
        """
        if not self.api_key:
            return {"error": "API key not configured"}
            
        url = f"{self.base_url}/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"  # Celsius, meters/sec for wind
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                "location": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
                "wind_speed": data["wind"]["speed"],
                "wind_direction": data["wind"].get("deg", 0),
                "visibility": data.get("visibility", 0) / 1000,  # Convert to km
                "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]),
                "sunset": datetime.fromtimestamp(data["sys"]["sunset"]),
                "timestamp": datetime.now()
            }
            
        except requests.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
        except KeyError as e:
            return {"error": f"Unexpected API response format: {str(e)}"}
    
    def get_forecast(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Get 5-day forecast for given coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dict containing forecast data
        """
        if not self.api_key:
            return {"error": "API key not configured"}
            
        url = f"{self.base_url}/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Process forecast data into daily summaries
            daily_forecasts = []
            current_date = None
            daily_data = {}
            
            for item in data["list"]:
                forecast_date = datetime.fromtimestamp(item["dt"]).date()
                
                # New day - save previous and start new
                if current_date != forecast_date:
                    if daily_data:
                        daily_forecasts.append(daily_data)
                    
                    daily_data = {
                        "date": forecast_date,
                        "temps": [item["main"]["temp"]],
                        "descriptions": [item["weather"][0]["description"]],
                        "icons": [item["weather"][0]["icon"]],
                        "humidity": [item["main"]["humidity"]],
                        "wind_speed": [item["wind"]["speed"]],
                        "rain_chance": item.get("pop", 0) * 100  # Probability of precipitation
                    }
                    current_date = forecast_date
                else:
                    # Add to current day
                    daily_data["temps"].append(item["main"]["temp"])
                    daily_data["descriptions"].append(item["weather"][0]["description"])
                    daily_data["icons"].append(item["weather"][0]["icon"])
                    daily_data["humidity"].append(item["main"]["humidity"])
                    daily_data["wind_speed"].append(item["wind"]["speed"])
                    daily_data["rain_chance"] = max(daily_data["rain_chance"], item.get("pop", 0) * 100)
            
            # Add the last day
            if daily_data:
                daily_forecasts.append(daily_data)
            
            # Calculate daily summaries
            processed_forecasts = []
            for day in daily_forecasts[:7]:  # Limit to 7 days
                processed_forecasts.append({
                    "date": day["date"],
                    "temp_high": max(day["temps"]),
                    "temp_low": min(day["temps"]),
                    "description": max(set(day["descriptions"]), key=day["descriptions"].count),  # Most common
                    "icon": max(set(day["icons"]), key=day["icons"].count),  # Most common
                    "humidity": sum(day["humidity"]) // len(day["humidity"]),  # Average
                    "wind_speed": sum(day["wind_speed"]) / len(day["wind_speed"]),  # Average
                    "rain_chance": day["rain_chance"]
                })
            
            return {
                "location": data["city"]["name"],
                "country": data["city"]["country"],
                "forecasts": processed_forecasts,
                "timestamp": datetime.now()
            }
            
        except requests.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
        except KeyError as e:
            return {"error": f"Unexpected API response format: {str(e)}"}

def get_user_location() -> Dict[str, Any]:
    """
    Get user's location using IP geolocation (free service)
    
    Returns:
        Dict containing lat, lon, city info
    """
    try:
        # Using ipapi.co free service (1000 requests/day)
        response = requests.get("https://ipapi.co/json/", timeout=5)
        response.raise_for_status()
        data = response.json()
        
        return {
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "city": data["city"],
            "region": data["region"],
            "country": data["country_name"]
        }
        
    except requests.RequestException as e:
        # Fallback to a default location (you can change this)
        return {
            "latitude": 45.5017,  # Montreal as example
            "longitude": -73.5673,
            "city": "Montreal",
            "region": "Quebec",
            "country": "Canada",
            "error": f"Could not detect location: {str(e)}"
        }
