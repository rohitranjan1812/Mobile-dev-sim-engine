"""
API Server for Property Risk Assessment Simulation
Provides RESTful API endpoints for simulation and analysis.
"""
from flask import Flask, request, jsonify
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sim_engine import SimulationEngine, SimulationConfig
from risk_assessment import RiskAssessor
from price_optimizer import PriceOptimizer


app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200


@app.route('/api/v1/simulate', methods=['POST'])
def run_simulation():
    """
    Run a new simulation.
    
    Request body:
    {
        "num_samples": 1000,
        "hazard_weight": 0.4,
        "vulnerability_weight": 0.3,
        "exposure_weight": 0.3,
        "random_seed": 42
    }
    """
    try:
        data = request.get_json()
        
        # Create configuration
        config_params = {
            'num_samples': data.get('num_samples', 1000),
            'batch_size': data.get('batch_size', 100),
            'random_seed': data.get('random_seed'),
            'hazard_weight': data.get('hazard_weight', 0.4),
            'vulnerability_weight': data.get('vulnerability_weight', 0.3),
            'exposure_weight': data.get('exposure_weight', 0.3),
        }
        
        config = SimulationConfig(**config_params)
        
        # Run simulation
        engine = SimulationEngine(config)
        simulation_data = engine.run_simulation()
        
        # Assess risk
        assessor = RiskAssessor(config)
        risk_data = assessor.assess_simulation_data(simulation_data)
        risk_stats = assessor.get_risk_statistics(risk_data['risk_score'])
        
        # Calculate prices
        optimizer = PriceOptimizer(config)
        price_stats = optimizer.get_price_statistics(risk_data['risk_score'])
        
        return jsonify({
            'status': 'success',
            'num_samples': config.num_samples,
            'risk_statistics': risk_stats,
            'price_statistics': price_stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/v1/assess-risk', methods=['POST'])
def assess_risk():
    """
    Assess risk for given property factors.
    
    Request body:
    {
        "hazard": [0.5, 0.6, 0.3],
        "vulnerability": [0.4, 0.5, 0.2],
        "exposure": [0.3, 0.4, 0.1],
        "weights": {
            "hazard": 0.4,
            "vulnerability": 0.3,
            "exposure": 0.3
        }
    }
    """
    try:
        data = request.get_json()
        
        hazard = np.array(data['hazard'])
        vulnerability = np.array(data['vulnerability'])
        exposure = np.array(data['exposure'])
        
        weights = data.get('weights', {})
        config = SimulationConfig(
            hazard_weight=weights.get('hazard', 0.4),
            vulnerability_weight=weights.get('vulnerability', 0.3),
            exposure_weight=weights.get('exposure', 0.3)
        )
        
        assessor = RiskAssessor(config)
        risk_scores = assessor.calculate_risk_score(hazard, vulnerability, exposure)
        categories = assessor.categorize_risk(risk_scores)
        
        return jsonify({
            'status': 'success',
            'risk_scores': risk_scores.tolist(),
            'risk_categories': categories.tolist()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/v1/optimize-price', methods=['POST'])
def optimize_price():
    """
    Calculate optimized prices for properties.
    
    Request body:
    {
        "risk_scores": [0.2, 0.5, 0.8],
        "base_price": 250000
    }
    """
    try:
        data = request.get_json()
        
        risk_scores = np.array(data['risk_scores'])
        base_price = data.get('base_price', 250000.0)
        
        config = SimulationConfig(base_property_price=base_price)
        optimizer = PriceOptimizer(config)
        
        prices = optimizer.calculate_price(risk_scores)
        
        return jsonify({
            'status': 'success',
            'prices': prices.tolist()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/v1/optimize-portfolio', methods=['POST'])
def optimize_portfolio():
    """
    Optimize property portfolio selection.
    
    Request body:
    {
        "risk_scores": [0.2, 0.5, 0.8, 0.3],
        "budget": 1000000,
        "risk_tolerance": 0.5
    }
    """
    try:
        data = request.get_json()
        
        risk_scores = np.array(data['risk_scores'])
        budget = data['budget']
        risk_tolerance = data.get('risk_tolerance', 0.5)
        
        config = SimulationConfig()
        optimizer = PriceOptimizer(config)
        
        result = optimizer.optimize_portfolio(risk_scores, budget, risk_tolerance)
        
        return jsonify({
            'status': 'success',
            'portfolio': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
