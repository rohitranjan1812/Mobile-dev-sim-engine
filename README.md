# Mobile-dev-sim-engine

A full-stack simulation tool for property risk assessment and price optimization.

## Overview

This simulation engine generates billions of random data points to assess property risks based on hazard, vulnerability, and exposure factors. It provides price optimization recommendations based on comprehensive risk analysis.

## Architecture

The system follows a modular architecture:

- **Simulation Engine**: Core component for generating random data and running simulations
- **Risk Assessment Module**: Analyzes hazard, vulnerability, and exposure factors
- **Price Optimization Module**: Calculates optimal property pricing based on risk profiles
- **API Layer**: RESTful API for accessing simulation results
- **Testing Infrastructure**: Comprehensive test suite for validation

## Features

- Random data generation for billions of simulation points
- Multi-factor risk assessment (hazard, vulnerability, and exposure)
- Property price optimization algorithms
- Configurable simulation parameters
- RESTful API for integration
- Comprehensive testing framework

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

## Usage

### Running Simulations

```python
from sim_engine.simulation import SimulationEngine
from sim_engine.config import SimulationConfig

# Configure simulation
config = SimulationConfig(
    num_samples=1000000,
    hazard_weight=0.4,
    vulnerability_weight=0.3,
    exposure_weight=0.3
)

# Run simulation
engine = SimulationEngine(config)
results = engine.run_simulation()
```

### API Server

```bash
# Start the API server
python src/api/server.py
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
```

## Project Structure

```
.
├── src/
│   ├── sim_engine/        # Core simulation engine
│   ├── risk_assessment/   # Risk analysis modules
│   ├── price_optimizer/   # Price optimization
│   └── api/               # API layer
├── tests/                 # Test suite
├── config/                # Configuration files
└── docs/                  # Documentation
```

## Configuration

The system uses configuration files to define simulation parameters and technical architecture. See `config/simulation_config.yaml` for details.

## License

MIT License