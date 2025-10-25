"""
Tests for Simulation Engine
"""
import pytest
import numpy as np
from src.sim_engine.simulation import SimulationEngine, DataGenerator
from src.sim_engine.config import SimulationConfig


def test_data_generator_batch():
    """Test data generator produces correct batch size."""
    config = SimulationConfig(num_samples=1000, random_seed=42)
    generator = DataGenerator(config)
    
    batch = generator.generate_batch(100)
    
    assert 'hazard' in batch
    assert 'vulnerability' in batch
    assert 'exposure' in batch
    assert len(batch['hazard']) == 100
    assert len(batch['vulnerability']) == 100
    assert len(batch['exposure']) == 100


def test_data_generator_ranges():
    """Test data generator respects configured ranges."""
    config = SimulationConfig(
        num_samples=1000,
        random_seed=42,
        hazard_min=0.2,
        hazard_max=0.8,
        vulnerability_min=0.1,
        vulnerability_max=0.9
    )
    generator = DataGenerator(config)
    
    batch = generator.generate_batch(1000)
    
    assert np.all(batch['hazard'] >= 0.2)
    assert np.all(batch['hazard'] <= 0.8)
    assert np.all(batch['vulnerability'] >= 0.1)
    assert np.all(batch['vulnerability'] <= 0.9)


def test_data_generator_reproducibility():
    """Test that same seed produces same results."""
    config1 = SimulationConfig(num_samples=100, random_seed=42)
    config2 = SimulationConfig(num_samples=100, random_seed=42)
    
    gen1 = DataGenerator(config1)
    gen2 = DataGenerator(config2)
    
    batch1 = gen1.generate_batch(100)
    batch2 = gen2.generate_batch(100)
    
    np.testing.assert_array_equal(batch1['hazard'], batch2['hazard'])
    np.testing.assert_array_equal(batch1['vulnerability'], batch2['vulnerability'])
    np.testing.assert_array_equal(batch1['exposure'], batch2['exposure'])


def test_simulation_engine_basic():
    """Test basic simulation engine functionality."""
    config = SimulationConfig(num_samples=500, batch_size=100, random_seed=42)
    engine = SimulationEngine(config)
    
    result = engine.run_simulation()
    
    assert 'hazard' in result
    assert 'vulnerability' in result
    assert 'exposure' in result
    assert len(result['hazard']) == 500
    assert len(result['vulnerability']) == 500
    assert len(result['exposure']) == 500


def test_simulation_engine_batching():
    """Test that batching works correctly with various sample sizes."""
    # Test when samples perfectly divide by batch size
    config = SimulationConfig(num_samples=1000, batch_size=100, random_seed=42)
    engine = SimulationEngine(config)
    result = engine.run_simulation()
    assert len(result['hazard']) == 1000
    
    # Test when samples don't perfectly divide by batch size
    config = SimulationConfig(num_samples=1050, batch_size=100, random_seed=42)
    engine = SimulationEngine(config)
    result = engine.run_simulation()
    assert len(result['hazard']) == 1050


def test_simulation_streaming():
    """Test streaming data generation."""
    config = SimulationConfig(num_samples=500, batch_size=100, random_seed=42)
    engine = SimulationEngine(config)
    
    batches = list(engine.generate_streaming())
    
    assert len(batches) == 5  # 500 samples / 100 batch_size
    
    # Check each batch has correct size
    for i, batch in enumerate(batches[:-1]):
        assert len(batch['hazard']) == 100
    
    # Last batch should also be 100 in this case
    assert len(batches[-1]['hazard']) == 100


def test_simulation_streaming_with_callback():
    """Test streaming with callback function."""
    config = SimulationConfig(num_samples=300, batch_size=100, random_seed=42)
    engine = SimulationEngine(config)
    
    callback_count = []
    
    def callback(batch, batch_num, total_batches):
        callback_count.append(batch_num)
        assert batch_num < total_batches
        assert 'hazard' in batch
    
    batches = list(engine.generate_streaming(callback=callback))
    
    assert len(callback_count) == 3  # 300 samples / 100 batch_size
    assert batches is not None
