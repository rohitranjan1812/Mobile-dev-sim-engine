"""
Example: Large Scale Streaming Simulation
Demonstrates streaming data generation for very large simulations.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sim_engine import SimulationEngine, SimulationConfig
from risk_assessment import RiskAssessor
from price_optimizer import PriceOptimizer
import numpy as np


def main():
    print("=" * 60)
    print("Large Scale Streaming Simulation")
    print("=" * 60)
    
    # Configure for large-scale simulation
    config = SimulationConfig(
        num_samples=1000000,  # 1 million samples
        batch_size=10000,
        random_seed=42
    )
    
    print(f"\nConfiguration:")
    print(f"  Total Samples: {config.num_samples:,}")
    print(f"  Batch Size: {config.batch_size:,}")
    print(f"  Number of Batches: {config.num_samples // config.batch_size:,}")
    
    # Initialize processors
    engine = SimulationEngine(config)
    assessor = RiskAssessor(config)
    optimizer = PriceOptimizer(config)
    
    # Accumulate statistics
    total_risk = 0.0
    total_price = 0.0
    min_risk = float('inf')
    max_risk = float('-inf')
    min_price = float('inf')
    max_price = float('-inf')
    processed_samples = 0
    
    print("\nProcessing batches...")
    
    # Process in streaming fashion
    for i, batch in enumerate(engine.generate_streaming()):
        # Calculate risk scores for this batch
        risk_scores = assessor.calculate_risk_score(
            batch['hazard'],
            batch['vulnerability'],
            batch['exposure']
        )
        
        # Calculate prices for this batch
        prices = optimizer.calculate_price(risk_scores)
        
        # Update statistics
        total_risk += np.sum(risk_scores)
        total_price += np.sum(prices)
        min_risk = min(min_risk, np.min(risk_scores))
        max_risk = max(max_risk, np.max(risk_scores))
        min_price = min(min_price, np.min(prices))
        max_price = max(max_price, np.max(prices))
        processed_samples += len(batch['hazard'])
        
        # Progress update every 10 batches
        if (i + 1) % 10 == 0:
            progress = (processed_samples / config.num_samples) * 100
            print(f"  Batch {i + 1}: {processed_samples:,} samples ({progress:.1f}%) processed")
    
    # Calculate final statistics
    avg_risk = total_risk / processed_samples
    avg_price = total_price / processed_samples
    
    print("\n" + "=" * 60)
    print("Results:")
    print("=" * 60)
    print(f"\nTotal Samples Processed: {processed_samples:,}")
    print(f"\nRisk Statistics:")
    print(f"  Average: {avg_risk:.4f}")
    print(f"  Min: {min_risk:.4f}")
    print(f"  Max: {max_risk:.4f}")
    print(f"\nPrice Statistics:")
    print(f"  Average: ${avg_price:,.2f}")
    print(f"  Min: ${min_price:,.2f}")
    print(f"  Max: ${max_price:,.2f}")
    print(f"  Total Value: ${total_price:,.2f}")
    
    print("\n" + "=" * 60)
    print("Streaming Simulation Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
