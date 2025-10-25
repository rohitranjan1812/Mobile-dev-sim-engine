"""
Example: Basic Simulation
Demonstrates how to run a basic property risk simulation.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sim_engine import SimulationEngine, SimulationConfig
from risk_assessment import RiskAssessor
from price_optimizer import PriceOptimizer


def main():
    print("=" * 60)
    print("Property Risk Assessment Simulation")
    print("=" * 60)
    
    # Configure simulation
    config = SimulationConfig(
        num_samples=10000,
        batch_size=1000,
        random_seed=42,
        hazard_weight=0.4,
        vulnerability_weight=0.3,
        exposure_weight=0.3,
        base_property_price=250000.0
    )
    
    print(f"\nConfiguration:")
    print(f"  Samples: {config.num_samples:,}")
    print(f"  Batch Size: {config.batch_size:,}")
    print(f"  Risk Weights: H={config.hazard_weight}, V={config.vulnerability_weight}, E={config.exposure_weight}")
    print(f"  Base Price: ${config.base_property_price:,.2f}")
    
    # Step 1: Run simulation
    print(f"\n[1/4] Generating {config.num_samples:,} random data points...")
    engine = SimulationEngine(config)
    simulation_data = engine.run_simulation()
    print(f"  ✓ Generated data for {len(simulation_data['hazard']):,} properties")
    
    # Step 2: Assess risk
    print(f"\n[2/4] Assessing risk factors...")
    assessor = RiskAssessor(config)
    risk_data = assessor.assess_simulation_data(simulation_data)
    risk_stats = assessor.get_risk_statistics(risk_data['risk_score'])
    
    print(f"  Risk Statistics:")
    print(f"    Mean: {risk_stats['mean']:.4f}")
    print(f"    Median: {risk_stats['median']:.4f}")
    print(f"    Std Dev: {risk_stats['std']:.4f}")
    print(f"    Min: {risk_stats['min']:.4f}")
    print(f"    Max: {risk_stats['max']:.4f}")
    print(f"    95th Percentile: {risk_stats['percentile_95']:.4f}")
    
    # Step 3: Calculate prices
    print(f"\n[3/4] Calculating optimized prices...")
    optimizer = PriceOptimizer(config)
    prices = optimizer.calculate_price(risk_data['risk_score'])
    price_stats = optimizer.get_price_statistics(risk_data['risk_score'])
    
    print(f"  Price Statistics:")
    print(f"    Mean: ${price_stats['mean']:,.2f}")
    print(f"    Median: ${price_stats['median']:,.2f}")
    print(f"    Min: ${price_stats['min']:,.2f}")
    print(f"    Max: ${price_stats['max']:,.2f}")
    print(f"    Total Value: ${price_stats['total_value']:,.2f}")
    
    # Step 4: Optimize portfolio
    print(f"\n[4/4] Optimizing portfolio...")
    portfolio = optimizer.optimize_portfolio(
        risk_data['risk_score'],
        budget=5000000.0,
        risk_tolerance=0.5
    )
    
    print(f"  Portfolio Results:")
    print(f"    Budget: $5,000,000.00")
    print(f"    Risk Tolerance: 0.5")
    print(f"    Properties Selected: {portfolio['num_properties']}")
    print(f"    Total Cost: ${portfolio['total_cost']:,.2f}")
    print(f"    Remaining Budget: ${portfolio['remaining_budget']:,.2f}")
    print(f"    Average Risk: {portfolio['average_risk']:.4f}")
    
    print("\n" + "=" * 60)
    print("Simulation Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
