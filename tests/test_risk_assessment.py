"""
Tests for Risk Assessment Module
"""
import pytest
import numpy as np
from src.risk_assessment.assessor import RiskAssessor
from src.sim_engine.config import SimulationConfig


def test_risk_score_calculation():
    """Test basic risk score calculation."""
    config = SimulationConfig(
        hazard_weight=0.4,
        vulnerability_weight=0.3,
        exposure_weight=0.3
    )
    assessor = RiskAssessor(config)
    
    hazard = np.array([0.5])
    vulnerability = np.array([0.6])
    exposure = np.array([0.4])
    
    risk_score = assessor.calculate_risk_score(hazard, vulnerability, exposure)
    
    expected = 0.4 * 0.5 + 0.3 * 0.6 + 0.3 * 0.4
    np.testing.assert_almost_equal(risk_score[0], expected)


def test_risk_score_arrays():
    """Test risk score calculation with arrays."""
    config = SimulationConfig()
    assessor = RiskAssessor(config)
    
    hazard = np.array([0.2, 0.5, 0.8])
    vulnerability = np.array([0.3, 0.6, 0.9])
    exposure = np.array([0.1, 0.4, 0.7])
    
    risk_scores = assessor.calculate_risk_score(hazard, vulnerability, exposure)
    
    assert len(risk_scores) == 3
    assert np.all(risk_scores >= 0.0)
    assert np.all(risk_scores <= 1.0)


def test_assess_simulation_data():
    """Test assessment of simulation data."""
    config = SimulationConfig()
    assessor = RiskAssessor(config)
    
    simulation_data = {
        'hazard': np.array([0.5, 0.6, 0.7]),
        'vulnerability': np.array([0.4, 0.5, 0.6]),
        'exposure': np.array([0.3, 0.4, 0.5])
    }
    
    result = assessor.assess_simulation_data(simulation_data)
    
    assert 'risk_score' in result
    assert 'hazard' in result
    assert 'vulnerability' in result
    assert 'exposure' in result
    assert len(result['risk_score']) == 3


def test_risk_categorization():
    """Test risk categorization."""
    config = SimulationConfig()
    assessor = RiskAssessor(config)
    
    risk_scores = np.array([0.1, 0.3, 0.6, 0.9])
    categories = assessor.categorize_risk(risk_scores)
    
    assert categories[0] == 0  # Low (< 0.25)
    assert categories[1] == 1  # Medium (0.25-0.5)
    assert categories[2] == 2  # High (0.5-0.75)
    assert categories[3] == 3  # Very High (>= 0.75)


def test_risk_statistics():
    """Test risk statistics calculation."""
    config = SimulationConfig()
    assessor = RiskAssessor(config)
    
    risk_scores = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    stats = assessor.get_risk_statistics(risk_scores)
    
    assert 'mean' in stats
    assert 'median' in stats
    assert 'std' in stats
    assert 'min' in stats
    assert 'max' in stats
    assert 'percentile_25' in stats
    assert 'percentile_75' in stats
    assert 'percentile_90' in stats
    assert 'percentile_95' in stats
    assert 'percentile_99' in stats
    
    assert stats['mean'] == pytest.approx(0.55, rel=0.01)
    assert stats['median'] == pytest.approx(0.55, rel=0.01)
    assert stats['min'] == 0.1
    assert stats['max'] == 1.0
