"""
Integration Tests for Full Simulation Pipeline
"""
import pytest
import numpy as np
from src.sim_engine import SimulationEngine, SimulationConfig
from src.risk_assessment import RiskAssessor
from src.price_optimizer import PriceOptimizer


def test_full_simulation_pipeline():
    """Test complete simulation pipeline from data generation to pricing."""
    # Configure simulation
    config = SimulationConfig(
        num_samples=1000,
        batch_size=100,
        random_seed=42,
        hazard_weight=0.4,
        vulnerability_weight=0.3,
        exposure_weight=0.3
    )
    
    # Step 1: Generate simulation data
    engine = SimulationEngine(config)
    simulation_data = engine.run_simulation()
    
    assert len(simulation_data['hazard']) == 1000
    assert len(simulation_data['vulnerability']) == 1000
    assert len(simulation_data['exposure']) == 1000
    
    # Step 2: Assess risk
    assessor = RiskAssessor(config)
    risk_data = assessor.assess_simulation_data(simulation_data)
    
    assert 'risk_score' in risk_data
    assert len(risk_data['risk_score']) == 1000
    
    # Step 3: Get risk statistics
    risk_stats = assessor.get_risk_statistics(risk_data['risk_score'])
    
    assert 0.0 <= risk_stats['mean'] <= 1.0
    assert 0.0 <= risk_stats['median'] <= 1.0
    assert risk_stats['min'] >= 0.0
    assert risk_stats['max'] <= 1.0
    
    # Step 4: Calculate prices
    optimizer = PriceOptimizer(config)
    prices = optimizer.calculate_price(risk_data['risk_score'])
    
    assert len(prices) == 1000
    assert np.all(prices > 0)
    
    # Step 5: Get price statistics
    price_stats = optimizer.get_price_statistics(risk_data['risk_score'])
    
    assert price_stats['mean'] > 0
    assert price_stats['total_value'] > 0
    
    # Step 6: Optimize portfolio
    portfolio = optimizer.optimize_portfolio(
        risk_data['risk_score'],
        budget=1000000.0,
        risk_tolerance=0.5
    )
    
    assert portfolio['total_cost'] <= 1000000.0
    if portfolio['num_properties'] > 0:
        assert portfolio['average_risk'] <= 0.5


def test_large_scale_simulation():
    """Test simulation with larger dataset."""
    config = SimulationConfig(
        num_samples=10000,
        batch_size=1000,
        random_seed=123
    )
    
    engine = SimulationEngine(config)
    simulation_data = engine.run_simulation()
    
    assessor = RiskAssessor(config)
    risk_data = assessor.assess_simulation_data(simulation_data)
    
    optimizer = PriceOptimizer(config)
    prices = optimizer.calculate_price(risk_data['risk_score'])
    
    assert len(prices) == 10000
    assert len(risk_data['risk_score']) == 10000


def test_streaming_pipeline():
    """Test streaming data generation with processing."""
    config = SimulationConfig(
        num_samples=5000,
        batch_size=500,
        random_seed=42
    )
    
    engine = SimulationEngine(config)
    assessor = RiskAssessor(config)
    optimizer = PriceOptimizer(config)
    
    total_batches = 0
    total_samples = 0
    
    for batch in engine.generate_streaming():
        # Process each batch
        risk_scores = assessor.calculate_risk_score(
            batch['hazard'],
            batch['vulnerability'],
            batch['exposure']
        )
        prices = optimizer.calculate_price(risk_scores)
        
        total_batches += 1
        total_samples += len(batch['hazard'])
        
        assert len(risk_scores) == len(batch['hazard'])
        assert len(prices) == len(batch['hazard'])
    
    assert total_samples == 5000
    assert total_batches == 10


def test_different_weight_configurations():
    """Test pipeline with different risk weight configurations."""
    weight_configs = [
        (0.5, 0.3, 0.2),
        (0.33, 0.34, 0.33),
        (0.6, 0.2, 0.2)
    ]
    
    for h_w, v_w, e_w in weight_configs:
        config = SimulationConfig(
            num_samples=500,
            random_seed=42,
            hazard_weight=h_w,
            vulnerability_weight=v_w,
            exposure_weight=e_w
        )
        
        engine = SimulationEngine(config)
        data = engine.run_simulation()
        
        assessor = RiskAssessor(config)
        risk_data = assessor.assess_simulation_data(data)
        
        optimizer = PriceOptimizer(config)
        prices = optimizer.calculate_price(risk_data['risk_score'])
        
        assert len(prices) == 500
        assert np.all(prices > 0)


def test_risk_price_correlation():
    """Test that higher risk leads to lower prices."""
    config = SimulationConfig(
        num_samples=100,
        random_seed=42,
        base_property_price=200000.0,
        risk_penalty_factor=0.5
    )
    
    engine = SimulationEngine(config)
    data = engine.run_simulation()
    
    assessor = RiskAssessor(config)
    risk_data = assessor.assess_simulation_data(data)
    
    optimizer = PriceOptimizer(config)
    prices = optimizer.calculate_price(risk_data['risk_score'])
    
    # Sort by risk
    sorted_indices = np.argsort(risk_data['risk_score'])
    sorted_risks = risk_data['risk_score'][sorted_indices]
    sorted_prices = prices[sorted_indices]
    
    # Check that prices generally decrease as risk increases
    # Use correlation coefficient
    correlation = np.corrcoef(sorted_risks, sorted_prices)[0, 1]
    assert correlation < 0  # Negative correlation (higher risk = lower price)
