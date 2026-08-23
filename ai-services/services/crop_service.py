import logging
import os
import joblib
from flask import Blueprint, request, jsonify
from core.response_formatter import format_success, format_error
from core.service_registry import registry
from interfaces.prediction_interface import PredictionInterface
from core.knowledge_loader import knowledge_loader
from reasoning.crop_reasoner import CropReasoner

crop_bp = Blueprint('crop', __name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../models/crop_model.pkl')
SCALER_PATH = os.path.join(os.path.dirname(__file__), '../models/crop_scaler.pkl')

class RealCropPredictor(PredictionInterface):
    def load_model(self):
        from core.config import Config
        self.model = joblib.load(Config.CROP_MODEL_PATH)
        if os.path.exists(Config.CROP_SCALER_PATH):
            self.scaler = joblib.load(Config.CROP_SCALER_PATH)
        else:
            self.scaler = None

    def preprocess(self, input_data):
        import pandas as pd
        df = pd.DataFrame([{
            'N': input_data.get('nitrogen', 50.0),
            'P': input_data.get('phosphorus', 50.0),
            'K': input_data.get('potassium', 50.0),
            'temperature': input_data.get('temperature', 25.0),
            'humidity': input_data.get('humidity', 70.0),
            'ph': input_data.get('ph', 6.5),
            'rainfall': input_data.get('rainfall', 100.0)
        }])
        
        if self.scaler:
            X = self.scaler.transform(df)
        else:
            X = df
        return X

    def load_knowledge(self, processed_data):
        return knowledge_loader.load('crop', 'requirements') or {}

    def reason(self, processed_data, knowledge):
        probs = self.model.predict_proba(processed_data)[0]
        classes = self.model.classes_
        return CropReasoner.reason_ml(probs, classes, knowledge)

    def calculate_confidence(self, reasoning):
        return CropReasoner.calculate_confidence(reasoning, is_ml=True)

    def generate_explanation(self, reasoning, confidence):
        return CropReasoner.generate_explanation(reasoning, confidence, is_ml=True)

    def format_response(self, reasoning, confidence, explanation):
        # Map internal standardized output back to the original expected API structure
        decisions = reasoning.get("decision", [])
        res = []
        for d in decisions:
            res.append({
                "crop": d.get("crop"),
                "confidence": d.get("confidence"),
                "reasoning": f"Based on ML model prediction ({d.get('confidence')}% match).",
                "icon": d.get("icon")
            })
        return res

try:
    registry.register('crop', RealCropPredictor())
except Exception as e:
    logging.info(f"Warning: Failed to load RealCropPredictor due to Exception: {e}. Falling back to mock predictor.")
    from mock.predictors import MockCropPredictor
    registry.register('crop', MockCropPredictor())

@crop_bp.route('/crop-recommend', methods=['POST'])
def crop_recommend():
    data = request.json
    if not data:
        return format_error("No JSON provided", 422)
    
    required_fields = ['nitrogen', 'phosphorus', 'potassium', 'ph', 'rainfall', 'temperature', 'humidity']
    for field in required_fields:
        if field not in data:
            return format_error(f"Missing field: {field}", 422)

    try:
        predictor = registry.get('crop')
        recommendations = predictor.predict(data)
        return jsonify(format_success({"recommendations": recommendations}))
    except Exception as e:
        return format_error(str(e), 500)
