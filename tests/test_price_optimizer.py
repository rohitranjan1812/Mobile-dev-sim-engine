"""
Tests for Price Optimizer Module
"""
import pytest
import numpy as np
from src.price_optimizer.optimizer import PriceOptimizer
from src.sim_engine.config import SimulationConfig


def test_basic_price_calculation():
    """Test basic price calculation."""
    config = SimulationConfig(
        base_property_price=250000.0,
        risk_penalty_factor=0.5
    )
    optimizer = PriceOptimizer(config)
    
    # Low risk should result in high price
    low_risk = np.array([0.0])
    high_price = optimizer.calculate_price(low_risk)
    assert high_price[0] == pytest.approx(250000.0)
    
    # High risk should result in lower price
    high_risk = np.array([1.0])
    low_price = optimizer.calculate_price(high_risk)
    assert low_price[0] == pytest.approx(125000.0)


def test_price_minimum_threshold():
    """Test that prices don't go below minimum threshold."""
    config = SimulationConfig(
        base_property_price=100000.0,
        risk_penalty_factor=2.0  # Very high penalty
    )
    optimizer = PriceOptimizer(config)
    
    # Even with very high risk, price should be at least 10% of base
    very_high_risk = np.array([1.0])
    prices = optimizer.calculate_price(very_high_risk)
    
    assert prices[0] >= 10000.0  # 10% of base price


def test_price_calculation_array():
    """Test price calculation with arrays."""
    config = SimulationConfig(base_property_price=200000.0)
    optimizer = PriceOptimizer(config)
    
    risk_scores = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
    prices = optimizer.calculate_price(risk_scores)
    
    assert len(prices) == 5
    # Prices should decrease as risk increases
    assert prices[0] > prices[1] > prices[2] > prices[3] > prices[4]


def test_custom_base_price():
    """Test using custom base price."""
    config = SimulationConfig()
    optimizer = PriceOptimizer(config)
    
    risk_scores = np.array([0.0])
    prices = optimizer.calculate_price(risk_scores, base_price=500000.0)
    
    assert prices[0] == pytest.approx(500000.0)


def test_portfolio_optimization_basic():
    """Test basic portfolio optimization."""
    config = SimulationConfig(base_property_price=100000.0)
    optimizer = PriceOptimizer(config)
    
    risk_scores = np.array([0.2, 0.3, 0.4, 0.5, 0.6])
    budget = 300000.0
    risk_tolerance = 0.5
    
    result = optimizer.optimize_portfolio(risk_scores, budget, risk_tolerance)
    
    assert 'selected_indices' in result
    assert 'total_cost' in result
    assert 'average_risk' in result
    assert 'num_properties' in result
    assert 'remaining_budget' in result
    
    assert result['total_cost'] <= budget
    assert result['average_risk'] <= risk_tolerance


def test_portfolio_optimization_no_eligible():
    """Test portfolio optimization when no properties meet risk tolerance."""
    config = SimulationConfig()
    optimizer = PriceOptimizer(config)
    
    # All properties have high risk
    risk_scores = np.array([0.8, 0.9, 1.0])
    budget = 500000.0
    risk_tolerance = 0.5  # Very low tolerance
    
    result = optimizer.optimize_portfolio(risk_scores, budget, risk_tolerance)
    
    assert len(result['selected_indices']) == 0
    assert result['total_cost'] == 0.0
    assert result['num_properties'] == 0


def test_portfolio_optimization_budget_constraint():
    """Test that portfolio optimization respects budget."""
    config = SimulationConfig(base_property_price=100000.0)
    optimizer = PriceOptimizer(config)
    
    risk_scores = np.array([0.1, 0.2, 0.3, 0.4])
    small_budget = 150000.0  # Can only afford 1-2 properties
    
    result = optimizer.optimize_portfolio(risk_scores, small_budget, risk_tolerance=1.0)
    
    assert result['total_cost'] <= small_budget
    assert result['num_properties'] <= 2


def test_price_statistics():
    """Test price statistics calculation."""
    config = SimulationConfig(base_property_price=200000.0)
    optimizer = PriceOptimizer(config)
    
    risk_scores = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
    stats = optimizer.get_price_statistics(risk_scores)
    
    assert 'mean' in stats
    assert 'median' in stats
    assert 'std' in stats
    assert 'min' in stats
    assert 'max' in stats
    assert 'total_value' in stats
    
    assert stats['max'] == pytest.approx(200000.0)
    assert stats['min'] > 0
    assert stats['total_value'] > 0
