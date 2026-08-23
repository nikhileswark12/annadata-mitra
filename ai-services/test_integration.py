import logging
import pytest
from app import app
import io

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    res = client.get('/health')
    assert res.status_code == 200
    data = res.get_json()
    assert data['status'] == 'success'
    assert 'predictors' in data['data']

def test_crop_recommend(client):
    payload = {
        "nitrogen": 100, "phosphorus": 50, "potassium": 50,
        "temperature": 25, "humidity": 70, "ph": 6.5, "rainfall": 200
    }
    res = client.post('/crop-recommend', json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data['status'] == 'success'
    assert 'recommendations' in data['data']
    assert len(data['data']['recommendations']) == 3

def test_vision_detect(client):
    data = {
        'image': (io.BytesIO(b"fake image data 1234567890"), 'test.jpg')
    }
    res = client.post('/disease-detect', data=data, content_type='multipart/form-data')
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data['status'] == 'success'
    assert 'disease' in json_data['data']

def test_market_insights(client):
    payload = {
        "crop": "wheat",
        "location": "Ahmedabad",
        "quantity": 100
    }
    res = client.post('/market-insights', json=payload)
    data = res.get_json()
    if res.status_code != 200:
        logging.info(f"Error 500 from market_insights: {data}")
    assert res.status_code == 200
    assert data['status'] == 'success'
    assert 'currentPrice' in data['data']
    assert len(data['data']['markets']) == 5
