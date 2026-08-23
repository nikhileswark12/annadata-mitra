"""
Crop Planning Agent — Rule-based recommendation engine.

Algorithm:
  For each of 22 crops, score how many of 7 parameters (N, P, K,
  pH, temp, humidity, rainfall) fall within the ICAR ideal range.
  Score = matched_params / 7 * 100
  Return top 3 crops sorted by score descending.

When train_crop_model.py has been run and crop_model.pkl exists,
the try_load_model() path activates and uses RandomForest instead.
The output shape is identical — zero frontend changes needed.
"""

import os
import logging
from agents.base_agent import BaseAgent
from core.knowledge_loader import knowledge_loader
from reasoning.crop_reasoner import CropReasoner

logger = logging.getLogger(__name__)
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../models/crop_model.pkl')
SCALER_PATH = os.path.join(os.path.dirname(__file__), '../models/crop_scaler.pkl')


class CropAgent(BaseAgent):

    def __init__(self):
        super().__init__('CropAgent')
        self.model = None
        self.scaler = None
        self.try_load_model(MODEL_PATH)

    def _load_model_file(self, path: str):
        import joblib
        self.model = joblib.load(path)
        self.scaler = joblib.load(SCALER_PATH)
        logger.info("CropAgent: RandomForest model loaded ✅")

    def validate(self, data: dict) -> list:
        errors = []
        required = {
            'nitrogen':    (0, 140),
            'phosphorus':  (0, 145),
            'potassium':   (0, 205),
            'ph':          (0, 14),
            'rainfall':    (0, 3000),
            'temperature': (-10, 60),
            'humidity':    (0, 100),
        }
        for field, (lo, hi) in required.items():
            if field not in data:
                errors.append(f"'{field}' is required")
                continue
            try:
                val = float(data[field])
                if not (lo <= val <= hi):
                    errors.append(
                        f"'{field}' must be between {lo} and {hi}, got {val}"
                    )
            except (TypeError, ValueError):
                errors.append(f"'{field}' must be a number, got '{data[field]}'")
        return errors

    def process(self, data: dict) -> dict:
        inp = {
            'N':        float(data['nitrogen']),
            'P':        float(data['phosphorus']),
            'K':        float(data['potassium']),
            'pH':       float(data['ph']),
            'temp':     float(data['temperature']),
            'humidity': float(data['humidity']),
            'rainfall': float(data['rainfall']),
        }

        if self.model and self.scaler:
            return self._predict_ml(inp, data)
        return self._predict_rules(inp, data)

    def _predict_rules(self, inp: dict, raw: dict) -> dict:
        crop_knowledge = knowledge_loader.load('crop', 'requirements') or {}
        params = knowledge_loader.load('crop', 'params') or {}
        
        reasoning = CropReasoner.reason_rules(inp, crop_knowledge, params)
        return self._format_agent_response(reasoning, raw, 'rule-based')

    def _predict_ml(self, inp: dict, raw: dict) -> dict:
        import numpy as np
        features = [[
            inp['N'], inp['P'], inp['K'],
            inp['temp'], inp['humidity'], inp['pH'], inp['rainfall']
        ]]
        scaled = self.scaler.transform(features)
        probas = self.model.predict_proba(scaled)[0]
        classes = self.model.classes_
        crop_knowledge = knowledge_loader.load('crop', 'requirements') or {}
        
        reasoning = CropReasoner.reason_ml(probas, classes, crop_knowledge)
        return self._format_agent_response(reasoning, raw, 'ml-model')

    def _format_agent_response(self, reasoning: dict, raw: dict, source: str) -> dict:
        is_ml = (source == 'ml-model')
        conf = CropReasoner.calculate_confidence(reasoning, is_ml=is_ml)
        expl = CropReasoner.generate_explanation(reasoning, conf, is_ml=is_ml)
        
        recommendations = []
        for dec in reasoning.get("decision", []):
            recommendations.append({
                'crop':       dec.get("crop"),
                'confidence': dec.get("confidence"),
                'reasoning':  dec.get("reasoning", expl.get("why")),
                'icon':       dec.get("icon"),
                'season':     dec.get("season", ""),
                'sowing':     dec.get("sowing", ""),
                'harvest':    dec.get("harvest", "")
            })
            
        note = 'Rule-based ICAR agronomic engine. Accuracy improves after ML model training.' if not is_ml else ''
        result = {
            'recommendations': recommendations,
            'location': raw.get('location', ''),
            'source': source
        }
        if note:
            result['note'] = note
        return result

