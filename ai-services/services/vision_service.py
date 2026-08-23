import logging
import os
import json
from flask import Blueprint, request, jsonify
from core.response_formatter import format_success, format_error
from core.service_registry import registry
from interfaces.prediction_interface import PredictionInterface
from core.knowledge_loader import knowledge_loader
from reasoning.vision_reasoner import VisionReasoner

vision_bp = Blueprint('vision', __name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../models/vision_model.h5')
CLASS_NAMES_PATH = os.path.join(os.path.dirname(__file__), '../models/class_names.json')

class RealVisionPredictor(PredictionInterface):
    def load_model(self):
        from core.config import Config
        import tensorflow as tf
        self.model = tf.keras.models.load_model(Config.VISION_MODEL_PATH)
        with open(Config.VISION_CLASS_NAMES_PATH, 'r') as f:
            self.class_names = json.load(f)

    def preprocess(self, input_data):
        from PIL import Image
        import numpy as np
        
        input_data.seek(0)
        img = Image.open(input_data).convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array

    def reason(self, processed_data, knowledge):
        preds = self.model.predict(processed_data)[0]
        return VisionReasoner.reason(preds, self.class_names)

    def load_knowledge(self, processed_data):
        return knowledge_loader.load('vision', 'disease_knowledge') or {}

    def calculate_confidence(self, reasoning):
        if "decision" in reasoning:
            return VisionReasoner.calculate_confidence(reasoning)
        return {"score": 87, "level": "Medium", "basis": "Mock Image Hash"}
        
    def generate_explanation(self, reasoning, confidence):
        knowledge = self.load_knowledge(None)
        if "decision" in reasoning:
            return VisionReasoner.generate_explanation(reasoning, confidence, knowledge)
        
        disease = reasoning
        k = knowledge.get(disease, {})
        return {
            "what": f"Diagnosis: {disease}",
            "why": k.get("description", f"AI model predicted {disease} based on leaf symptoms."),
            "factors": k.get("treatment", "1. Remove affected leaves.\n2. Ensure proper spacing for aeration.\n3. Apply appropriate fungicide if necessary."),
            "severity": k.get("severity", "Unknown")
        }

    def format_response(self, reasoning, confidence, explanation):
        if "decision" in reasoning:
            dec = reasoning["decision"]
            return {
                "disease": dec.get("disease"),
                "confidence": confidence.get("score"),
                "severity": explanation.get("severity", "Unknown"),
                "description": explanation.get("why"),
                "treatment": explanation.get("factors")
            }
        # For mock predictor fallback
        return {
            "disease": reasoning,
            "confidence": confidence.get("score"),
            "severity": explanation.get("severity", "Unknown"),
            "description": explanation.get("why"),
            "treatment": explanation.get("factors")
        }

try:
    if os.path.exists(MODEL_PATH) and os.path.exists(CLASS_NAMES_PATH):
        registry.register('vision', RealVisionPredictor())
    else:
        from mock.predictors import MockVisionPredictor
        registry.register('vision', MockVisionPredictor())
except Exception as e:
    logging.info(f"Warning: Failed to load RealVisionPredictor due to Exception: {e}. Falling back to mock predictor.")
    from mock.predictors import MockVisionPredictor
    registry.register('vision', MockVisionPredictor())

@vision_bp.route('/disease-detect', methods=['POST'])
def disease_detect():
    if 'image' not in request.files:
        return format_error("No image provided", 400)
    
    file = request.files['image']
    if not file or file.filename == '':
        return format_error("No selected file", 400)
        
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in {'.png', '.jpg', '.jpeg'} and not file.mimetype.startswith('image/'):
        return format_error("Invalid file type", 400)
        
    try:
        predictor = registry.get('vision')
        diagnosis = predictor.predict(file)
        return jsonify(format_success(diagnosis))
    except Exception as e:
        return format_error(str(e), 500)
