import logging
from flask import Blueprint, request, jsonify
from core.response_formatter import format_success, format_error
from core.service_registry import registry
from interfaces.prediction_interface import PredictionInterface
from core.knowledge_loader import knowledge_loader
from reasoning.strategist_reasoner import StrategistReasoner

strategist_bp = Blueprint('strategist', __name__)

class StrategistPredictor(PredictionInterface):
    def load_model(self):
        # Strategist is an orchestration agent, it has no native ML model of its own.
        pass

    def preprocess(self, input_data):
        import logging
        goal = str(input_data.get("goal", ""))
        location = str(input_data.get("location", ""))
        crop = str(input_data.get("crop", ""))
        
        context = {
            "goal": goal,
            "location": location,
            "crop": crop
        }
        
        upstream = {}
        source_status = {
            "crop": "unavailable",
            "weather": "unavailable",
            "market": "unavailable"
        }
        
        # Crop Agent
        try:
            if "nitrogen" in input_data:
                crop_predictor = registry.get("crop")
                upstream["crop"] = crop_predictor.predict(input_data)
                source_status["crop"] = "available"
            else:
                # Crop suitability requires the same complete soil/environment
                # inputs as the standalone Crop Planning agent. Do not call the
                # predictor with implicit defaults and present that as evidence.
                source_status["crop"] = "insufficient_input"
        except Exception as e:
            logging.error(f"Strategist Crop orchestration error: {e}")
            source_status["crop"] = "failed"

        # Weather Agent
        try:
            if location:
                weather_predictor = registry.get("weather")
                upstream["weather"] = weather_predictor.predict(input_data)
                source_status["weather"] = "available"
            else:
                source_status["weather"] = "insufficient_input"
        except Exception as e:
            logging.error(f"Strategist Weather orchestration error: {e}")
            source_status["weather"] = "failed"

        # Market Agent
        try:
            if crop and location:
                market_predictor = registry.get("market")
                upstream["market"] = market_predictor.predict(input_data)
                source_status["market"] = "available"
            else:
                source_status["market"] = "insufficient_input"
        except Exception as e:
            logging.error(f"Strategist Market orchestration error: {e}")
            source_status["market"] = "failed"
            
        return {
            "context": context,
            "upstream": upstream,
            "source_status": source_status
        }

    def load_knowledge(self, processed_data):
        return {
            "metadata": knowledge_loader.load('strategist', 'metadata') or {},
            "placeholder": knowledge_loader.load('strategist', 'placeholder') or {},
            "synthesis_rules": knowledge_loader.load('strategist', 'synthesis_rules') or {}
        }

    def reason(self, processed_data, knowledge):
        return StrategistReasoner.reason(processed_data, knowledge)

    def calculate_confidence(self, reasoning):
        return StrategistReasoner.calculate_confidence(reasoning)

    def generate_explanation(self, reasoning, confidence):
        return StrategistReasoner.generate_explanation(reasoning, confidence)

    def format_response(self, reasoning, confidence, explanation):
        decision = reasoning.get("decision", {})
        
        return {
            "crop": str(decision.get("crop", "")),
            "location": str(decision.get("location", "")),
            "season": str(decision.get("season", "")),
            "confidence": int(confidence.get("score", 0)),
            "cropAdvice": str(decision.get("cropAdvice", "")),
            "marketTiming": str(decision.get("marketTiming", "")),
            "weatherRisk": str(decision.get("weatherRisk", "")),
            "farmAdvisory": str(decision.get("farmAdvisory", "")),
            "actions": decision.get("actions", []),
            "explanation": explanation
        }

class MockStrategistPredictor(PredictionInterface):
    def load_model(self):
        pass

    def preprocess(self, input_data):
        return input_data

    def load_knowledge(self, processed_data):
        return {}

    def reason(self, processed_data, knowledge):
        return {
            "decision": {
                "crop": "Mock Crop",
                "location": "Mock Location",
                "season": "Mock Season",
                "cropAdvice": "Mock crop advice.",
                "marketTiming": "Mock market timing.",
                "weatherRisk": "Mock weather risk.",
                "farmAdvisory": "Mock farm advisory.",
                "actions": ["Mock action 1"]
            },
            "factors": []
        }

    def calculate_confidence(self, reasoning):
        return {"score": 0, "level": "Low", "basis": "Mock fallback"}

    def generate_explanation(self, reasoning, confidence):
        return {"what": "Mocked", "why": "Fallback", "factors": "Mock"}

    def format_response(self, reasoning, confidence, explanation):
        decision = reasoning.get("decision", {})
        
        return {
            "crop": str(decision.get("crop", "")),
            "location": str(decision.get("location", "")),
            "season": str(decision.get("season", "")),
            "confidence": int(confidence.get("score", 0)),
            "cropAdvice": str(decision.get("cropAdvice", "")),
            "marketTiming": str(decision.get("marketTiming", "")),
            "weatherRisk": str(decision.get("weatherRisk", "")),
            "farmAdvisory": str(decision.get("farmAdvisory", "")),
            "actions": decision.get("actions", []),
            "explanation": explanation
        }

try:
    registry.register('strategist', StrategistPredictor())
except Exception as e:
    logging.info(f"Warning: Failed to load StrategistPredictor due to Exception: {e}. Falling back to mock predictor.")
    registry.register('strategist', MockStrategistPredictor())

@strategist_bp.route('/strategist-plan', methods=['POST'])
def strategist_plan():
    data = request.json
    if not data:
        return format_error("No JSON provided", 422)
    
    try:
        predictor = registry.get('strategist')
        result = predictor.predict(data)
        return jsonify(format_success(result))
    except Exception as e:
        return format_error(str(e), 500)
