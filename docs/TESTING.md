# Testing Guide

## Overview

The Mobile Dev Sim Engine includes a comprehensive test suite with 39 tests covering all major components. The tests achieve 95% code coverage.

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test Files

```bash
# Configuration tests
pytest tests/test_config.py

# Simulation engine tests
pytest tests/test_simulation.py

# Risk assessment tests
pytest tests/test_risk_assessment.py

# Price optimizer tests
pytest tests/test_price_optimizer.py

# API tests
pytest tests/test_api.py

# Integration tests
pytest tests/test_integration.py
```

### Run with Verbose Output

```bash
pytest -v
```

### Run with Coverage Report

```bash
pytest --cov=src --cov-report=html
```

This generates an HTML coverage report in the `htmlcov/` directory.

### Run Specific Test

```bash
pytest tests/test_simulation.py::test_data_generator_batch
```

## Test Organization

### Unit Tests

- **test_config.py**: Tests for configuration validation
- **test_simulation.py**: Tests for data generation and simulation engine
- **test_risk_assessment.py**: Tests for risk scoring and statistics
- **test_price_optimizer.py**: Tests for price calculation and portfolio optimization

### Integration Tests

- **test_integration.py**: Tests for complete simulation pipeline
- **test_api.py**: Tests for REST API endpoints

## Test Categories

### Configuration Tests

- Default configuration values
- Custom configuration
- Weight validation (must sum to 1.0)
- Range validation
- Positive value validation

### Simulation Tests

- Batch generation
- Range constraints
- Reproducibility with random seeds
- Batching with various sizes
- Streaming data generation

### Risk Assessment Tests

- Risk score calculation
- Array processing
- Simulation data assessment
- Risk categorization
- Statistical calculations

### Price Optimization Tests

- Basic price calculation
- Minimum price threshold
- Array processing
- Custom base prices
- Portfolio optimization
- Budget constraints

### Integration Tests

- Full simulation pipeline
- Large-scale simulations (10,000+ samples)
- Streaming pipeline
- Different weight configurations
- Risk-price correlation

### API Tests

- Health check endpoint
- Simulation endpoint
- Risk assessment endpoint
- Price optimization endpoint
- Portfolio optimization endpoint
- Error handling

## Writing New Tests

Follow the existing test structure:

```python
def test_feature_name():
    """Test description."""
    # Arrange
    config = SimulationConfig(...)
    
    # Act
    result = some_function(...)
    
    # Assert
    assert result == expected_value
```

## Continuous Testing

The test suite is designed for continuous integration. All tests should:
- Run quickly (< 1 second each)
- Be independent
- Use reproducible random seeds where applicable
- Clean up resources

## Performance Testing

For large-scale performance tests:

```python
import time

def test_large_scale_performance():
    """Test performance with large dataset."""
    config = SimulationConfig(num_samples=1000000)
    
    start = time.time()
    engine = SimulationEngine(config)
    data = engine.run_simulation()
    elapsed = time.time() - start
    
    assert elapsed < 10.0  # Should complete in < 10 seconds
```

## Coverage Goals

- Maintain > 90% code coverage
- Cover all critical paths
- Test edge cases and error conditions
- Validate input/output contracts

## Running Tests in CI/CD

Example GitHub Actions workflow:

```yaml
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest --cov=src --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```
