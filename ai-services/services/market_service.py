import logging
import os
import pandas as pd
from flask import Blueprint, request, jsonify
from core.response_formatter import format_success, format_error
from core.service_registry import registry
from interfaces.prediction_interface import PredictionInterface
from core.knowledge_loader import knowledge_loader
from mock.predictors import MockMarketPredictor
from reasoning.market_reasoner import MarketReasoner

market_bp = Blueprint('market', __name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), '../datasets/mandi/mandi_prices.csv')

class RealMarketPredictor(PredictionInterface):
    def load_model(self):
        from core.config import Config
        if os.path.exists(Config.MANDI_CSV_PATH):
            self.df = pd.read_csv(Config.MANDI_CSV_PATH, low_memory=False)
        else:
            self.df = None

    def preprocess(self, input_data):
        return input_data.get('crop', '').strip().lower()

    def load_knowledge(self, processed_data):
        if self.df is not None:
            crop_df = self.df[self.df['Crops'].str.lower() == processed_data]
            if not crop_df.empty:
                return crop_df
        return None

    def reason(self, processed_data, knowledge):
        if knowledge is not None:
            advice_rules = knowledge_loader.load('market', 'advice_rules') or {}
            return MarketReasoner.reason(processed_data, knowledge, advice_rules)
        
        # Fallback to synthetic if crop not found or CSV missing
        from mock.predictors import MockMarketPredictor
        mock_predictor = MockMarketPredictor()
        mock_knowledge = mock_predictor.load_knowledge(processed_data)
        return mock_predictor.reason(processed_data, mock_knowledge)

    def calculate_confidence(self, reasoning):
        # mock predictor returns a flat dict, MarketReasoner returns standard struct
        if "decision" in reasoning:
            return MarketReasoner.calculate_confidence(reasoning)
        return {"score": 80, "level": "Medium", "basis": "Mock Data"}

    def generate_explanation(self, reasoning, confidence):
        if "decision" in reasoning:
            return MarketReasoner.generate_explanation(reasoning, confidence)
        return {"what": "Mocked advice", "why": "Synthetic data fallback", "factors": ""}

    def format_response(self, reasoning, confidence, explanation):
        if "decision" in reasoning:
            dec = reasoning["decision"]
            return {
                "currentPrice": dec.get("currentPrice"),
                "predictedPrice": dec.get("predictedPrice"),
                "advice": dec.get("advice"),
                "trendWatch": dec.get("trendWatch"),
                "demandInsight": dec.get("demandInsight"),
                "markets": reasoning.get("factors", []),
                "totalValue": None,
                "source": "csv-data"
            }
        # For mock predictor fallback
        return reasoning

from core.config import Config

try:
    if Config.USE_MOCK_MODELS:
        from mock.predictors import MockMarketPredictor
        registry.register('market', MockMarketPredictor())
        logging.info("Market service initialized with MockMarketPredictor (USE_MOCK_MODELS=True)")
    else:
        registry.register('market', RealMarketPredictor())
        logging.info("Market service initialized with RealMarketPredictor")
except Exception as e:
    logging.error(f"CRITICAL: Failed to load RealMarketPredictor due to Exception: {e}")

@market_bp.route('/market-insights', methods=['POST'])
def market_insights():
    data = request.json
    if not data:
        return format_error("No JSON provided", 422)
    
    if 'crop' not in data or 'location' not in data:
        return format_error("Missing crop or location", 422)
        
    try:
        predictor = registry.get('market')
        insights = predictor.predict(data)
        return jsonify(format_success(insights))
    except Exception as e:
        return format_error(str(e), 500)
