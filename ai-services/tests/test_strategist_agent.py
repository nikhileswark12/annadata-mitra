import pytest
import json
from unittest.mock import MagicMock, patch

from services.strategist_service import StrategistPredictor
from app import app
from core.service_registry import registry

@pytest.fixture
def strategist():
    return StrategistPredictor()

@pytest.fixture
def mock_crop_predictor():
    mock = MagicMock()
    mock.predict.return_value = {
        "recommendations": [{"crop": "wheat", "confidence": 95, "reasoning": "Suitable"}]
    }
    return mock

@pytest.fixture
def mock_weather_predictor():
    mock = MagicMock()
    mock.predict.return_value = {
        "location": "punjab",
        "crop": "wheat",
        "risks": [],
        "condition": "Sunny"
    }
    return mock

@pytest.fixture
def mock_market_predictor():
    mock = MagicMock()
    mock.predict.return_value = {
        "currentPrice": 2000,
        "advice": "Sell now",
        "markets": []
    }
    return mock

def test_1_full_orchestration(strategist, mock_crop_predictor, mock_weather_predictor, mock_market_predictor):
    with patch.object(registry, 'get') as mock_get:
        def get_predictor(name):
            if name == "crop": return mock_crop_predictor
            if name == "weather": return mock_weather_predictor
            if name == "market": return mock_market_predictor
            return None
        mock_get.side_effect = get_predictor
        
        result = strategist.predict({"goal": "profit", "location": "punjab", "crop": "wheat", "nitrogen": 50})
        
        assert result["crop"] == "wheat"
        assert result["confidence"] == 100
        assert "Crop suitability confirmed" in result["explanation"]["factors"][0]

def test_1b_insufficient_crop_input(strategist, mock_crop_predictor, mock_weather_predictor, mock_market_predictor):
    with patch.object(registry, 'get') as mock_get:
        def get_predictor(name):
            if name == "crop": return mock_crop_predictor
            if name == "weather": return mock_weather_predictor
            if name == "market": return mock_market_predictor
            return None
        mock_get.side_effect = get_predictor
        
        # Missing nitrogen, phosphorus, etc.
        result = strategist.predict({"goal": "profit", "location": "punjab", "crop": "wheat"})
        
        assert "Crop suitability could not be fully assessed" in result["cropAdvice"]
        assert result["confidence"] == 85 # 100 - 15 penalty

def test_2_crop_failure(strategist, mock_weather_predictor, mock_market_predictor):
    with patch.object(registry, 'get') as mock_get:
        def get_predictor(name):
            if name == "crop": raise Exception("Crop Agent failed")
            if name == "weather": return mock_weather_predictor
            if name == "market": return mock_market_predictor
            return None
        mock_get.side_effect = get_predictor
        
        result = strategist.predict({"goal": "profit", "location": "punjab", "crop": "wheat", "nitrogen": 50})
        assert "Crop suitability data unavailable" in result["cropAdvice"]
        assert result["confidence"] == 90 # base 100 - 10 penalty

def test_3_weather_failure(strategist, mock_crop_predictor, mock_market_predictor):
    with patch.object(registry, 'get') as mock_get:
        def get_predictor(name):
            if name == "crop": return mock_crop_predictor
            if name == "weather": raise Exception("Weather API down")
            if name == "market": return mock_market_predictor
            return None
        mock_get.side_effect = get_predictor
        
        result = strategist.predict({"goal": "profit", "location": "punjab", "crop": "wheat", "nitrogen": 50})
        assert "Weather data unavailable" in result["weatherRisk"]
        assert result["confidence"] == 70 # base 100 - 30 penalty

def test_4_market_failure(strategist, mock_crop_predictor, mock_weather_predictor):
    with patch.object(registry, 'get') as mock_get:
        def get_predictor(name):
            if name == "crop": return mock_crop_predictor
            if name == "weather": return mock_weather_predictor
            if name == "market": raise Exception("Market API down")
            return None
        mock_get.side_effect = get_predictor
        
        result = strategist.predict({"goal": "profit", "location": "punjab", "crop": "wheat", "nitrogen": 50})
        assert "Market intelligence unavailable" in result["marketTiming"]
        assert result["confidence"] == 80 # base 100 - 20 penalty

def test_5_multiple_failures(strategist, mock_weather_predictor):
    with patch.object(registry, 'get') as mock_get:
        def get_predictor(name):
            if name == "crop": raise Exception("Failed")
            if name == "weather": return mock_weather_predictor
            if name == "market": raise Exception("Failed")
            return None
        mock_get.side_effect = get_predictor
        
        result = strategist.predict({"goal": "profit", "location": "punjab", "crop": "wheat", "nitrogen": 50})
        assert "Crop suitability data unavailable" in result["cropAdvice"]
        assert "Market intelligence unavailable" in result["marketTiming"]
        assert result["confidence"] == 70 # 100 - 10 - 20 = 70

def test_6_all_agents_unavailable(strategist):
    with patch.object(registry, 'get', side_effect=Exception("Agent down")):
        result = strategist.predict({"goal": "profit", "location": "punjab", "crop": "wheat"})
        assert "Insufficient agricultural intelligence" in result["cropAdvice"]
        assert result["confidence"] == 0

def test_7_conflict_resolution(strategist, mock_crop_predictor):
    mock_weather_conflict = MagicMock()
    mock_weather_conflict.predict.return_value = {
        "location": "punjab",
        "risks": [{"risk": "Flood", "severity": "High Risk", "advice": "Harvest immediately."}]
    }
    
    mock_market_conflict = MagicMock()
    mock_market_conflict.predict.return_value = {
        "advice": "Wait to sell. Prices are rising."
    }
    
    with patch.object(registry, 'get') as mock_get:
        def get_predictor(name):
            if name == "crop": return mock_crop_predictor
            if name == "weather": return mock_weather_conflict
            if name == "market": return mock_market_conflict
            return None
        mock_get.side_effect = get_predictor
        
        result = strategist.predict({"goal": "profit", "location": "punjab", "crop": "wheat", "nitrogen": 50})
        assert "Prioritize immediate harvest" in result["marketTiming"]
        assert "Conflict detected" in " ".join(result["explanation"]["factors"])
        assert result["confidence"] == 90 # 100 - 10 conflict penalty
        
        # Test deduplication and conflict action suppression
        action_texts = result["actions"]
        assert "Monitor market trends for optimal selling time." not in action_texts
        assert len(action_texts) == len(set(action_texts)) # Deduplicated

def test_8_confidence_calculation(strategist):
    # Tested inherently in partial failure tests, but explicit test here
    with patch.object(registry, 'get') as mock_get:
        mock_get.side_effect = Exception("Agent down")
        result = strategist.predict({"goal": "profit", "location": "punjab", "crop": "wheat"})
        assert result["confidence"] == 0
        assert "Failed to generate strategy" in result["explanation"]["what"]

def test_9_explanation_generation(strategist, mock_crop_predictor, mock_weather_predictor, mock_market_predictor):
    with patch.object(registry, 'get') as mock_get:
        def get_predictor(name):
            if name == "crop": return mock_crop_predictor
            if name == "weather": return mock_weather_predictor
            if name == "market": return mock_market_predictor
            return None
        mock_get.side_effect = get_predictor
        
        result = strategist.predict({"goal": "profit", "location": "punjab", "crop": "wheat", "nitrogen": 50})
        assert "Synthesized integrated strategy using 3 AI agent" in result["explanation"]["what"]

def test_10_response_contract(strategist, mock_crop_predictor, mock_weather_predictor, mock_market_predictor):
    with patch.object(registry, 'get') as mock_get:
        def get_predictor(name):
            if name == "crop": return mock_crop_predictor
            if name == "weather": return mock_weather_predictor
            if name == "market": return mock_market_predictor
            return None
        mock_get.side_effect = get_predictor
        
        result = strategist.predict({"goal": "profit", "location": "punjab", "crop": "wheat"})
        expected_keys = {"crop", "location", "season", "confidence", "cropAdvice", "marketTiming", "weatherRisk", "farmAdvisory", "actions", "explanation"}
        assert set(result.keys()) == expected_keys
        assert isinstance(result["actions"], list)
        assert isinstance(result["confidence"], int)

def test_11_service_registration():
    predictor = registry.get("strategist")
    assert predictor is not None
    assert hasattr(predictor, 'predict')

def test_12_api_endpoint(mock_crop_predictor, mock_weather_predictor, mock_market_predictor):
    client = app.test_client()
    
    with patch.object(registry, 'get') as mock_get:
        def get_predictor(name):
            if name == "crop": return mock_crop_predictor
            if name == "weather": return mock_weather_predictor
            if name == "market": return mock_market_predictor
            if name == "strategist": return StrategistPredictor()
            return None
        mock_get.side_effect = get_predictor
        
        response = client.post('/strategist-plan', json={
            "goal": "profit", "location": "punjab", "crop": "wheat"
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["data"]["crop"] == "wheat"
