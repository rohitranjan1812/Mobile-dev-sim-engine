"""
Tests for API Endpoints
"""
import pytest
import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api.server import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'


def test_simulate_endpoint(client):
    """Test simulation endpoint."""
    request_data = {
        'num_samples': 1000,
        'hazard_weight': 0.4,
        'vulnerability_weight': 0.3,
        'exposure_weight': 0.3,
        'random_seed': 42
    }
    
    response = client.post(
        '/api/v1/simulate',
        data=json.dumps(request_data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['num_samples'] == 1000
    assert 'risk_statistics' in data
    assert 'price_statistics' in data


def test_simulate_endpoint_default_params(client):
    """Test simulation endpoint with default parameters."""
    response = client.post(
        '/api/v1/simulate',
        data=json.dumps({}),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'


def test_simulate_endpoint_invalid_weights(client):
    """Test simulation endpoint with invalid weights."""
    request_data = {
        'num_samples': 100,
        'hazard_weight': 0.5,
        'vulnerability_weight': 0.3,
        'exposure_weight': 0.3  # Sum > 1.0
    }
    
    response = client.post(
        '/api/v1/simulate',
        data=json.dumps(request_data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'


def test_assess_risk_endpoint(client):
    """Test risk assessment endpoint."""
    request_data = {
        'hazard': [0.5, 0.6, 0.3],
        'vulnerability': [0.4, 0.5, 0.2],
        'exposure': [0.3, 0.4, 0.1]
    }
    
    response = client.post(
        '/api/v1/assess-risk',
        data=json.dumps(request_data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert len(data['risk_scores']) == 3
    assert len(data['risk_categories']) == 3


def test_assess_risk_with_custom_weights(client):
    """Test risk assessment with custom weights."""
    request_data = {
        'hazard': [0.5],
        'vulnerability': [0.4],
        'exposure': [0.3],
        'weights': {
            'hazard': 0.5,
            'vulnerability': 0.3,
            'exposure': 0.2
        }
    }
    
    response = client.post(
        '/api/v1/assess-risk',
        data=json.dumps(request_data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'


def test_optimize_price_endpoint(client):
    """Test price optimization endpoint."""
    request_data = {
        'risk_scores': [0.2, 0.5, 0.8],
        'base_price': 250000
    }
    
    response = client.post(
        '/api/v1/optimize-price',
        data=json.dumps(request_data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert len(data['prices']) == 3
    # Prices should decrease as risk increases
    assert data['prices'][0] > data['prices'][1] > data['prices'][2]


def test_optimize_portfolio_endpoint(client):
    """Test portfolio optimization endpoint."""
    request_data = {
        'risk_scores': [0.2, 0.5, 0.8, 0.3],
        'budget': 1000000,
        'risk_tolerance': 0.5
    }
    
    response = client.post(
        '/api/v1/optimize-portfolio',
        data=json.dumps(request_data),
        content_type='application/json'
    )
    
    if response.status_code != 200:
        print("Error response:", json.loads(response.data))
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'portfolio' in data
    assert data['portfolio']['total_cost'] <= 1000000


def test_api_error_handling(client):
    """Test API error handling with missing data."""
    response = client.post(
        '/api/v1/assess-risk',
        data=json.dumps({}),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['status'] == 'error'
