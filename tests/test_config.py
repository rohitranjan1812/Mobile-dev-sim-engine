"""
Tests for Simulation Engine Configuration
"""
import pytest
from src.sim_engine.config import SimulationConfig


def test_default_config():
    """Test default configuration values."""
    config = SimulationConfig()
    
    assert config.num_samples == 1000000
    assert config.batch_size == 10000
    assert config.random_seed is None
    assert config.hazard_weight == 0.4
    assert config.vulnerability_weight == 0.3
    assert config.exposure_weight == 0.3
    assert config.base_property_price == 250000.0


def test_custom_config():
    """Test custom configuration values."""
    config = SimulationConfig(
        num_samples=5000,
        batch_size=500,
        random_seed=42,
        hazard_weight=0.5,
        vulnerability_weight=0.3,
        exposure_weight=0.2
    )
    
    assert config.num_samples == 5000
    assert config.batch_size == 500
    assert config.random_seed == 42
    assert config.hazard_weight == 0.5
    assert config.vulnerability_weight == 0.3
    assert config.exposure_weight == 0.2


def test_weights_validation():
    """Test that weights must sum to 1.0."""
    # Valid weights
    config = SimulationConfig(
        hazard_weight=0.5,
        vulnerability_weight=0.3,
        exposure_weight=0.2
    )
    assert config is not None
    
    # Invalid weights (don't sum to 1.0)
    with pytest.raises(ValueError, match="Risk factor weights must sum to 1.0"):
        SimulationConfig(
            hazard_weight=0.5,
            vulnerability_weight=0.3,
            exposure_weight=0.3
        )


def test_range_validation():
    """Test that min values must be less than max values."""
    with pytest.raises(ValueError, match="hazard_min must be less than hazard_max"):
        SimulationConfig(hazard_min=1.0, hazard_max=0.0)
    
    with pytest.raises(ValueError, match="vulnerability_min must be less than vulnerability_max"):
        SimulationConfig(vulnerability_min=1.0, vulnerability_max=0.0)
    
    with pytest.raises(ValueError, match="exposure_min must be less than exposure_max"):
        SimulationConfig(exposure_min=1.0, exposure_max=0.0)


def test_positive_values_validation():
    """Test that certain values must be positive."""
    with pytest.raises(ValueError, match="num_samples must be positive"):
        SimulationConfig(num_samples=0)
    
    with pytest.raises(ValueError, match="batch_size must be positive"):
        SimulationConfig(batch_size=-1)
    
    with pytest.raises(ValueError, match="base_property_price must be positive"):
        SimulationConfig(base_property_price=-100)
