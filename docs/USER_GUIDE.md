# User Guide

## Introduction

The Mobile Dev Sim Engine is a powerful simulation tool for property risk assessment and price optimization. It can generate billions of random data points to analyze risk factors and optimize property pricing.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/rohitranjan1812/Mobile-dev-sim-engine.git
cd Mobile-dev-sim-engine
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

## Quick Start

### Running Your First Simulation

```python
from sim_engine import SimulationEngine, SimulationConfig
from risk_assessment import RiskAssessor
from price_optimizer import PriceOptimizer

# Configure simulation
config = SimulationConfig(
    num_samples=10000,
    random_seed=42
)

# Generate data
engine = SimulationEngine(config)
data = engine.run_simulation()

# Assess risk
assessor = RiskAssessor(config)
risk_data = assessor.assess_simulation_data(data)

# Optimize prices
optimizer = PriceOptimizer(config)
prices = optimizer.calculate_price(risk_data['risk_score'])

print(f"Generated {len(prices)} property prices")
print(f"Average price: ${prices.mean():,.2f}")
```

### Using Example Scripts

Run the basic simulation example:
```bash
python examples/basic_simulation.py
```

Run the large-scale streaming example:
```bash
python examples/streaming_simulation.py
```

## Core Concepts

### Risk Factors

The simulation assesses three primary risk factors:

1. **Hazard**: External risk factors (natural disasters, location risks)
2. **Vulnerability**: Property-specific weaknesses
3. **Exposure**: Potential impact magnitude

Each factor is represented as a value between 0 (low risk) and 1 (high risk).

### Risk Score

The composite risk score is calculated as a weighted average:

```
Risk Score = (hazard_weight × hazard) + 
             (vulnerability_weight × vulnerability) + 
             (exposure_weight × exposure)
```

Default weights: Hazard=0.4, Vulnerability=0.3, Exposure=0.3

### Price Optimization

Property prices are adjusted based on risk:

```
Price = base_price × (1 - risk_penalty_factor × risk_score)
```

- Lower risk properties → Higher prices
- Higher risk properties → Lower prices

## Configuration

### Basic Configuration

```python
from sim_engine import SimulationConfig

config = SimulationConfig(
    num_samples=100000,      # Number of properties to simulate
    batch_size=10000,        # Processing batch size
    random_seed=42,          # For reproducibility
    hazard_weight=0.4,       # Risk factor weights
    vulnerability_weight=0.3,
    exposure_weight=0.3,
    base_property_price=250000.0,
    risk_penalty_factor=0.5
)
```

### Using YAML Configuration

See `config/simulation_config.yaml` for a complete configuration example.

## Common Use Cases

### Large-Scale Simulations

For billions of data points, use streaming:

```python
engine = SimulationEngine(config)

for batch in engine.generate_streaming():
    # Process each batch
    risk_scores = assessor.calculate_risk_score(
        batch['hazard'],
        batch['vulnerability'],
        batch['exposure']
    )
    prices = optimizer.calculate_price(risk_scores)
    # ... store or analyze results
```

### Portfolio Optimization

Select properties within budget and risk tolerance:

```python
portfolio = optimizer.optimize_portfolio(
    risk_scores=risk_data['risk_score'],
    budget=5000000.0,
    risk_tolerance=0.5
)

print(f"Selected {portfolio['num_properties']} properties")
print(f"Total cost: ${portfolio['total_cost']:,.2f}")
print(f"Average risk: {portfolio['average_risk']:.4f}")
```

### Custom Risk Weights

Adjust weights based on your needs:

```python
# Emphasize hazard more heavily
config = SimulationConfig(
    hazard_weight=0.6,
    vulnerability_weight=0.2,
    exposure_weight=0.2
)
```

### Statistical Analysis

Get detailed statistics:

```python
risk_stats = assessor.get_risk_statistics(risk_scores)
print(f"Mean risk: {risk_stats['mean']:.4f}")
print(f"95th percentile: {risk_stats['percentile_95']:.4f}")

price_stats = optimizer.get_price_statistics(risk_scores)
print(f"Total portfolio value: ${price_stats['total_value']:,.2f}")
```

## API Usage

Start the API server:

```bash
python src/api/server.py
```

Make requests:

```python
import requests

response = requests.post(
    'http://localhost:5000/api/v1/simulate',
    json={'num_samples': 5000, 'random_seed': 42}
)
data = response.json()
```

See [API Documentation](API.md) for complete endpoint details.

## Best Practices

### Memory Management

For very large simulations (billions of samples):
- Use streaming with `generate_streaming()`
- Process in batches
- Don't store all data in memory at once

### Reproducibility

Always set a random seed for reproducible results:

```python
config = SimulationConfig(random_seed=42)
```

### Performance

- Increase `batch_size` for better performance
- Use streaming for datasets > 10 million samples
- Consider parallel processing for independent batches

### Validation

Always validate configuration:

```python
try:
    config = SimulationConfig(
        hazard_weight=0.5,
        vulnerability_weight=0.3,
        exposure_weight=0.3  # Sum > 1.0, will raise error
    )
except ValueError as e:
    print(f"Configuration error: {e}")
```

## Troubleshooting

### Import Errors

If you encounter import errors, ensure you've installed the package:
```bash
pip install -e .
```

### Memory Issues

For large simulations, use streaming:
```python
engine = SimulationEngine(config)
for batch in engine.generate_streaming():
    # Process immediately, don't accumulate
    pass
```

### Performance Issues

- Reduce `num_samples` for testing
- Increase `batch_size` (default: 10000)
- Use NumPy operations (already optimized)

## Advanced Topics

### Custom Risk Models

Extend the `RiskAssessor` class:

```python
class CustomRiskAssessor(RiskAssessor):
    def calculate_risk_score(self, hazard, vulnerability, exposure):
        # Custom risk calculation
        return super().calculate_risk_score(hazard, vulnerability, exposure)
```

### Custom Price Models

Extend the `PriceOptimizer` class:

```python
class CustomPriceOptimizer(PriceOptimizer):
    def calculate_price(self, risk_scores, base_price=None):
        # Custom pricing logic
        return super().calculate_price(risk_scores, base_price)
```

## Getting Help

- See [API Documentation](API.md) for endpoint details
- See [Testing Guide](TESTING.md) for test information
- Check `config/architecture.md` for system design
- Review example scripts in `examples/`

## License

MIT License - see LICENSE file for details.
