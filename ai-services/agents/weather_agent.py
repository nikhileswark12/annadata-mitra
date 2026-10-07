"""
Weather Risk Agent — Pure local rule engine.
No API calls. Generates realistic synthetic seasonal weather from
location string hash + current month. Risk evaluation is deterministic.

Upgrade path: Replace _get_weather() with OpenWeatherMap API call.
Output shape stays identical — zero frontend changes needed.
"""

import hashlib
import logging
from datetime import datetime
from agents.base_agent import BaseAgent
from core.knowledge_loader import knowledge_loader
from reasoning.weather_reasoner import WeatherReasoner

logger = logging.getLogger(__name__)

# 10-minute in-memory cache: { location_key: (timestamp, weather_dict) }
_CACHE = {}
CACHE_TTL_SECONDS = 600


class WeatherAgent(BaseAgent):

    def __init__(self):
        super().__init__('WeatherAgent')

    def validate(self, data: dict) -> list:
        errors = []
        if not data.get('location') or len(str(data['location']).strip()) < 2:
            errors.append("'location' is required (minimum 2 characters)")
        return errors

    def process(self, data: dict) -> dict:
        location = str(data['location']).strip()
        crop = str(data.get('crop', 'crops')).strip()

        cache_key = location.lower()
        now = datetime.now().timestamp()
        if cache_key in _CACHE:
            ts, cached = _CACHE[cache_key]
            if now - ts < CACHE_TTL_SECONDS:
                return {**cached, 'crop': crop, 'cached': True}

        weather = self._get_weather(location)
        risks = self._evaluate_risks(weather, crop)

        result = {
            'location':    location,
            'crop':        crop,
            'temperature': weather['temperature'],
            'humidity':    weather['humidity'],
            'rainfall':    weather['rainfall'],
            'windSpeed':   weather['windSpeed'],
            'condition':   weather['condition'],
            'risks':       risks,
            'source':      'synthetic-seasonal',
            'note':        'Add OPENWEATHER_API_KEY to .env for live weather data.',
            'cached':      False,
        }
        _CACHE[cache_key] = (now, result)
        return result

    def _get_weather(self, location: str) -> dict:
        """
        Fetch live weather data from OpenWeatherMap if OPENWEATHER_API_KEY is present in env.
        Otherwise, fall back to generating deterministic realistic weather from location + season.
        """
        import os
        import json
        import urllib.request
        from urllib.parse import quote
        
        api_key = os.environ.get('OPENWEATHER_API_KEY')
        
        if api_key and api_key != 'your_actual_api_key_here':
            try:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={quote(location)}&appid={api_key}&units=metric"
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode())
                
                return {
                    'temperature': round(data['main']['temp'], 1),
                    'humidity': round(data['main']['humidity']),
                    'rainfall': round(data.get('rain', {}).get('1h', 0.0), 1),
                    'windSpeed': round(data['wind']['speed'] * 3.6, 1), # Convert m/s to km/h
                    'condition': data['weather'][0]['main'].title() if data.get('weather') else 'Clear',
                }
            except Exception as e:
                logger.error(f"OpenWeatherMap API error: {e}. Falling back to synthetic data.")

        # Fallback: Generate deterministic realistic weather from location + season
        month = datetime.now().month - 1  # 0-indexed
        baselines = knowledge_loader.load('weather', 'seasonal_baselines')
        base_temp, base_hum, base_rain, base_wind = baselines.get(str(month), (25, 60, 50, 10))

        # Use location hash to add realistic variance (±15% of base)
        h = int(hashlib.md5(location.lower().encode()).hexdigest(), 16)
        variance = lambda base, pct=0.15: round(
            base * (1 + ((h % 100) - 50) / 100 * pct * 2), 1
        )

        temp      = max(-5,  min(50, variance(base_temp, 0.12)))
        humidity  = max(10,  min(100, variance(base_hum, 0.18)))
        rainfall  = max(0,   variance(base_rain, 0.40))
        wind      = max(0,   variance(base_wind, 0.25))

        CONDITIONS = ['Clear', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Moderate Rain']
        cond_idx = 4 if rainfall > 50 else 3 if rainfall > 20 else 2 if humidity > 70 else 1
        condition = CONDITIONS[cond_idx]

        return {
            'temperature': round(temp, 1),
            'humidity':    round(humidity),
            'rainfall':    round(rainfall, 1),
            'windSpeed':   round(wind, 1),
            'condition':   condition,
        }

    def _evaluate_risks(self, weather: dict, crop: str) -> list:
        risk_rules = knowledge_loader.load('weather', 'risk_rules') or []
        no_risk_msg = knowledge_loader.load('weather', 'no_risk_message') or {}

        reasoning = WeatherReasoner.reason(weather, risk_rules, no_risk_msg)
        
        # Original system expects just the array of risks back
        return reasoning.get("decision", [])
