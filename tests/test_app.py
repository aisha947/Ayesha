# tests/test_app.py
import json
from Devops_Prac.app import app  # Adjust the import path

def test_train_endpoint(client):
    # Test the /train endpoint
    data = {'data': [20, 21, 22, 23, 24]}
    response = client.post('/train', json=data)
    assert response.status_code == 200
    result = response.get_json()
    assert 'message' in result
    assert result['message'] == 'Model trained successfully'

def test_predict_endpoint(client):
    # Test the /api/predict endpoint
    data = {'date': 16}  # Assuming you want to predict for the 16th day
    response = client.post('/api/predict', json=data)
    assert response.status_code == 200
    result = response.get_json()
    assert 'prediction' in result

def test_invalid_data_predict_endpoint(client):
    # Test the /api/predict endpoint with invalid data
    data = {'invalid_key': 16}
    response = client.post('/api/predict', json=data)
    assert response.status_code == 500
    result = response.get_json()
    assert 'error' in result

