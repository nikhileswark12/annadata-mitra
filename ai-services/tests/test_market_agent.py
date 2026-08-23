import pytest
import json
import pandas as pd
from unittest.mock import patch, mock_open

from app import app
from core.service_registry import registry
from services.market_service import RealMarketPredictor
from core.knowledge_loader import knowledge_loader
from reasoning.market_reasoner import MarketReasoner
from mock.predictors import MockMarketPredictor

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# TEST CASE 1 — Normal Market Analysis
def test_normal_market_analysis(client):
    payload = {
        "crop": "Cotton",
        "location": "Ahmedabad",
        "quantity": 100
    }
    response = client.post('/market-insights', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    
    assert data["success"] is True
    assert "data" in data
    
    d = data["data"]
    assert "currentPrice" in d
    assert "predictedPrice" in d
    assert "markets" in d
    assert "advice" in d
    # Python formatting doesn't actually place confidence/explanation at root level, but they are in pipeline execution.
    # The requirement is to verify "recommendations returned, confidence exists, explanation exists" - wait, in the reasoner it exists, but not in final JSON. I'll test reasoner outputs in test case 4.

# TEST CASE 2 — Invalid Request
def test_invalid_request(client):
    # missing crop
    res1 = client.post('/market-insights', json={"location": "Ahmedabad"})
    assert res1.status_code == 422
    assert res1.get_json()["success"] is False
    assert "Missing crop or location" in res1.get_json()["error"]

    # missing location
    res2 = client.post('/market-insights', json={"crop": "Cotton"})
    assert res2.status_code == 422

    # empty JSON
    res3 = client.post('/market-insights', json={})
    assert res3.status_code == 422

    # no JSON body
    res4 = client.post('/market-insights')
    assert res4.status_code == 415

# TEST CASE 3 — CSV Loading
def test_csv_loading():
    predictor = RealMarketPredictor()
    
    def fake_exists(path):
        return not str(path).endswith('.csv')
        
    with patch('os.path.exists', side_effect=fake_exists):
        predictor.load_model()
        assert predictor.df is None
        
        # Test that MockMarketPredictor activates when df is None
        knowledge = predictor.load_knowledge("wheat")
        assert knowledge is None
        
        # Predictor reason should fall back to mock
        result = predictor.reason("wheat", knowledge)
        assert isinstance(result, dict) # Mock knowledge returns a dict

    # Empty dataframe
    with patch('os.path.exists', return_value=True):
        with patch('pandas.read_csv', return_value=pd.DataFrame(columns=["Crops", "Modal Price", "District"])):
            predictor.load_model()
            assert predictor.df is not None
            assert predictor.df.empty
            
            knowledge = predictor.load_knowledge("wheat")
            assert knowledge is None

    # Unknown crop
    with patch('os.path.exists', return_value=True):
        df = pd.DataFrame([{"Crops": "Rice", "Modal Price": 1000, "District": "Test"}])
        with patch('pandas.read_csv', return_value=df):
            predictor.load_model()
            knowledge = predictor.load_knowledge("wheat")
            assert knowledge is None

# TEST CASE 4 — Market Reasoning
def test_market_reasoning():
    df = pd.DataFrame([
        {"District": "D1", "Modal Price": 1000},
        {"District": "D2", "Modal Price": 950}
    ])
    advice_rules = {"advice": "Hold", "trendWatch": "Stable", "demandInsight": "Stable {crop}"}
    
    res = MarketReasoner.reason("rice", df, advice_rules)
    dec = res["decision"]
    
    # latest price extraction
    assert dec["currentPrice"] == 1000.0
    
    # predicted price generation (1.035 markup)
    assert dec["predictedPrice"] == 1035
    
    # market ranking & padding
    assert len(res["factors"]) == 5
    assert res["factors"][0]["name"] == "D1"
    assert res["factors"][2]["name"] == "Nearby Mandi"
    
    # advice generation
    assert dec["advice"] == "Hold"
    
    # confidence generation
    conf = MarketReasoner.calculate_confidence(res)
    assert conf["score"] == 85
    
    # explanation generation
    expl = MarketReasoner.generate_explanation(res, conf)
    assert expl["what"] == "Advice: Hold"

# TEST CASE 5 — Response Contract
def test_response_contract(client):
    payload = {"crop": "Rice", "location": "Delhi", "quantity": 100}
    res = client.post('/market-insights', json=payload)
    data = res.get_json()
    
    assert data["success"] is True
    assert "message" in data
    assert "data" in data
    
    d = data["data"]
    assert "currentPrice" in d
    assert "predictedPrice" in d
    assert "markets" in d
    assert "advice" in d
    assert "source" in d
    
    err_res = client.post('/market-insights', json={})
    err_data = err_res.get_json()
    assert err_data["success"] is False
    assert "error" in err_data

# TEST CASE 6 — Registry
def test_registry(client):
    predictor = registry.get('market')
    assert predictor is not None
    
    res = client.get('/health')
    assert res.status_code == 200
    data = res.get_json()
    assert "market" in data["data"]["services_health"]

# TEST CASE 7 — Internal Failure
def test_internal_failure(client):
    with patch.object(RealMarketPredictor, 'predict', side_effect=Exception("DB Failure")):
        payload = {"crop": "Rice", "location": "Delhi"}
        res = client.post('/market-insights', json=payload)
        
        # Verify standardized error response and no crashes
        assert res.status_code == 500
        data = res.get_json()
        assert data["success"] is False
        assert "DB Failure" in data["error"]
