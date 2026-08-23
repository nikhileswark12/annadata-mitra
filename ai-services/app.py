import logging
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from core.config import Config
from core.response_formatter import format_success, format_error
from core.service_registry import registry
from mock.predictors import MockCropPredictor, MockVisionPredictor, MockMarketPredictor

from services.crop_service import crop_bp
from services.vision_service import vision_bp
from services.market_service import market_bp
from services.weather_service import weather_bp
from services.strategist_service import strategist_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(crop_bp)
app.register_blueprint(vision_bp)
app.register_blueprint(market_bp)
app.register_blueprint(weather_bp)
app.register_blueprint(strategist_bp)

@app.route('/health', methods=['GET'])
def health():
    predictors_info = {
        name: predictor.health() if hasattr(predictor, 'health') else type(predictor).__name__
        for name, predictor in registry._services.items()
    }
    return jsonify(format_success({
        "status": "ok", 
        "service": "annadata-mitra-ai",
        "services_health": predictors_info
    }))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=(Config.ENV == 'development'))