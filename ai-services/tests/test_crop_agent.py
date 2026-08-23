import pytest
import json
import importlib
from unittest.mock import patch, mock_open

from app import app
from core.service_registry import registry
from services.crop_service import RealCropPredictor
from core.knowledge_loader import knowledge_loader

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# TEST CASE 1 — Valid Crop Recommendation
def test_valid_crop_recommendation(client):
    payload = {
        "nitrogen": 90,
        "phosphorus": 42,
        "potassium": 43,
        "ph": 6.5,
        "rainfall": 202.9,
        "temperature": 20.8,
        "humidity": 82
    }
    response = client.post('/crop-recommend', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "recommendations" in data["data"]
    
    recs = data["data"]["recommendations"]
    assert len(recs) > 0
    assert "crop" in recs[0]
    assert "confidence" in recs[0]
    assert "reasoning" in recs[0]

# TEST CASE 2 — Invalid Input Handling
def test_invalid_input_handling(client):
    # Missing nitrogen
    payload_missing = {
        "phosphorus": 42,
        "potassium": 43,
        "ph": 6.5,
        "rainfall": 200,
        "temperature": 20,
        "humidity": 80
    }
    res1 = client.post('/crop-recommend', json=payload_missing)
    assert res1.status_code == 422
    assert res1.get_json()["success"] is False
    assert "Missing field: nitrogen" in res1.get_json()["error"]

    # No JSON body
    res2 = client.post('/crop-recommend')
    assert res2.status_code == 415

# TEST CASE 3 — Model Availability
def test_model_availability():
    predictor = registry.get('crop')
    assert predictor is not None
    assert getattr(predictor, '_initialized', False) is True
    # If the real model loaded, _fallback_active is False
    # If it failed during actual run, it might be True. But we just check it exists.

# TEST CASE 4 — Model Failure Fallback
def test_model_failure_fallback(client):
    with patch('joblib.load', side_effect=Exception("Simulated Model Failure")):
        import services.crop_service as crop_service
        # Re-run the try-except logic from crop_service manually to see if it registers MockCropPredictor
        predictor = crop_service.RealCropPredictor()
        try:
            registry.register('test_crop_fail', predictor)
        except Exception:
            from mock.predictors import MockCropPredictor
            registry.register('test_crop_fail', MockCropPredictor())
        
        fallback_predictor = registry.get('test_crop_fail')
        assert fallback_predictor.__class__.__name__ == 'MockCropPredictor'
        
        # Test the fallback execution
        payload = {
            "nitrogen": 90, "phosphorus": 42, "potassium": 43,
            "ph": 6.5, "rainfall": 200, "temperature": 20, "humidity": 80
        }
        res = fallback_predictor.predict(payload)
        assert len(res) > 0
        assert "crop" in res[0]

# TEST CASE 5 — Knowledge Loading
def test_knowledge_loading():
    # Load correctly
    data = knowledge_loader.load('crop', 'requirements')
    assert data is not None
    
    # Missing file handling
    with patch('os.path.exists', return_value=False):
        empty_data = knowledge_loader.load('crop', 'missing_file')
        assert empty_data is None

    # Invalid JSON handling
    with patch('builtins.open', mock_open(read_data="INVALID_JSON")):
        with patch('os.path.exists', return_value=True):
            with patch('os.path.getmtime', return_value=12345):
                invalid_data = knowledge_loader.load('crop', 'bad_json_file')
                assert invalid_data is None

# TEST CASE 6 — Response Contract
def test_response_contract(client):
    payload = {
        "nitrogen": 90, "phosphorus": 42, "potassium": 43,
        "ph": 6.5, "rainfall": 200, "temperature": 20, "humidity": 80
    }
    response = client.post('/crop-recommend', json=payload)
    data = response.get_json()
    
    # Internal & External schema success check
    assert "success" in data
    assert "message" in data
    assert "data" in data
    
    recs = data["data"]["recommendations"]
    for rec in recs:
        assert "crop" in rec
        assert "confidence" in rec
        assert "reasoning" in rec

    # Error contract
    err_res = client.post('/crop-recommend', json={})
    err_data = err_res.get_json()
    assert err_data["success"] is False
    assert "error" in err_data
