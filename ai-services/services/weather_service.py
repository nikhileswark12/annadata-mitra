import logging
from flask import Blueprint, request, jsonify
from core.response_formatter import format_success, format_error
from core.service_registry import registry
from interfaces.prediction_interface import PredictionInterface
from core.knowledge_loader import knowledge_loader
from reasoning.weather_reasoner import WeatherReasoner
from agents.weather_agent import WeatherAgent

weather_bp = Blueprint('weather', __name__)

class RealWeatherPredictor(PredictionInterface):
    def load_model(self):
        self.agent = WeatherAgent()

    def preprocess(self, input_data):
        location = str(input_data['location']).strip()
        crop = str(input_data.get('crop', 'crops')).strip()
        weather = self.agent._get_weather(location)
        return {
            "location": location,
            "crop": crop,
            "weather": weather
        }

    def load_knowledge(self, processed_data):
        return {
            "risk_rules": knowledge_loader.load('weather', 'risk_rules') or [],
            "no_risk_msg": knowledge_loader.load('weather', 'no_risk_message') or {}
        }

    def reason(self, processed_data, knowledge):
        weather = processed_data["weather"]
        reasoning = WeatherReasoner.reason(weather, knowledge["risk_rules"], knowledge["no_risk_msg"])
        reasoning["context"] = processed_data
        return reasoning

    def calculate_confidence(self, reasoning):
        return WeatherReasoner.calculate_confidence(reasoning)

    def generate_explanation(self, reasoning, confidence):
        return WeatherReasoner.generate_explanation(reasoning, confidence)

    def format_response(self, reasoning, confidence, explanation):
        context = reasoning.get("context", {})
        weather = context.get("weather", {})
        source = weather.get("source", "synthetic-fallback")

        if source == "openweathermap":
            note = "Live weather data fetched from OpenWeatherMap."
        elif source == "synthetic-fallback":
            note = "OpenWeatherMap was unavailable; deterministic seasonal fallback data was used."
        else:
            note = "Deterministic seasonal weather data is being used because OPENWEATHER_API_KEY is not configured."

        return {
            'location': context.get('location', ''),
            'crop': context.get('crop', 'crops'),
            'temperature': weather.get('temperature', 0),
            'humidity': weather.get('humidity', 0),
            'rainfall': weather.get('rainfall', 0),
            'windSpeed': weather.get('windSpeed', 0),
            'condition': weather.get('condition', ''),
            'risks': reasoning.get("decision", []),
            'source': source,
            'note': note,
            'cached': False,
        }

try:
    registry.register('weather', RealWeatherPredictor())
    logging.info("Weather service initialized with RealWeatherPredictor")
except Exception as e:
    logging.error(f"CRITICAL: Failed to load RealWeatherPredictor due to Exception: {e}")

@weather_bp.route('/weather-risk', methods=['POST'])
def weather_risk():
    data = request.json
    if not data:
        return format_error("No JSON provided", 422)

    if 'location' not in data or len(str(data['location']).strip()) < 2:
        return format_error("Missing field: location", 422)

    try:
        predictor = registry.get('weather')
        result = predictor.predict(data)
        return jsonify(format_success(result))
    except Exception as e:
        return format_error(str(e), 500)
