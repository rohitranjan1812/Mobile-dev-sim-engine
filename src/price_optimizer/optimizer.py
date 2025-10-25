"""
Price Optimization Module
Calculates optimal property prices based on risk assessment.
"""
import numpy as np
from typing import Dict, Optional, Tuple

try:
    from sim_engine.config import SimulationConfig
except ImportError:
    from ..sim_engine.config import SimulationConfig


class PriceOptimizer:
    """Optimizes property pricing based on risk factors."""
    
    def __init__(self, config: SimulationConfig):
        """
        Initialize the price optimizer.
        
        Args:
            config: Simulation configuration
        """
        self.config = config
    
    def calculate_price(
        self,
        risk_scores: np.ndarray,
        base_price: Optional[float] = None
    ) -> np.ndarray:
        """
        Calculate property prices based on risk scores.
        
        Lower risk properties have higher prices, higher risk properties have lower prices.
        
        Args:
            risk_scores: Array of risk scores (0-1)
            base_price: Base property price (uses config default if None)
            
        Returns:
            Array of optimized property prices
        """
        if base_price is None:
            base_price = self.config.base_property_price
        
        # Calculate risk adjustment: reduce price as risk increases
        # Price = base_price * (1 - risk_penalty_factor * risk_score)
        risk_adjustment = 1.0 - (self.config.risk_penalty_factor * risk_scores)
        
        # Ensure prices don't go below a minimum threshold (10% of base price)
        risk_adjustment = np.maximum(risk_adjustment, 0.1)
        
        prices = base_price * risk_adjustment
        
        return prices
    
    def optimize_portfolio(
        self,
        risk_scores: np.ndarray,
        budget: float,
        risk_tolerance: float = 0.5
    ) -> Dict[str, any]:
        """
        Optimize property portfolio selection within budget and risk tolerance.
        
        Args:
            risk_scores: Array of risk scores for properties
            budget: Total budget for portfolio
            risk_tolerance: Maximum acceptable average risk (0-1)
            
        Returns:
            Dictionary with selected property indices and portfolio statistics
        """
        prices = self.calculate_price(risk_scores)
        
        # Filter properties within risk tolerance
        eligible_mask = risk_scores <= risk_tolerance
        eligible_indices = np.where(eligible_mask)[0]
        
        if len(eligible_indices) == 0:
            return {
                'selected_indices': [],
                'total_cost': 0.0,
                'average_risk': 0.0,
                'num_properties': 0
            }
        
        eligible_prices = prices[eligible_indices]
        eligible_risks = risk_scores[eligible_indices]
        
        # Sort by best value (lowest risk per dollar)
        value_ratios = eligible_risks / eligible_prices
        sorted_indices = np.argsort(value_ratios)
        
        # Greedily select properties within budget
        selected = []
        total_cost = 0.0
        
        for idx in sorted_indices:
            property_price = eligible_prices[idx]
            if total_cost + property_price <= budget:
                selected.append(eligible_indices[idx])
                total_cost += property_price
        
        if not selected:
            return {
                'selected_indices': [],
                'total_cost': 0.0,
                'average_risk': 0.0,
                'num_properties': 0
            }
        
        selected_risks = risk_scores[selected]
        
        return {
            'selected_indices': [int(idx) for idx in selected],  # Convert to Python int
            'total_cost': float(total_cost),
            'average_risk': float(np.mean(selected_risks)),
            'num_properties': len(selected),
            'remaining_budget': float(budget - total_cost)
        }
    
    def get_price_statistics(
        self,
        risk_scores: np.ndarray
    ) -> Dict[str, float]:
        """
        Calculate statistics for optimized prices.
        
        Args:
            risk_scores: Array of risk scores
            
        Returns:
            Dictionary with price statistics
        """
        prices = self.calculate_price(risk_scores)
        
        return {
            'mean': float(np.mean(prices)),
            'median': float(np.median(prices)),
            'std': float(np.std(prices)),
            'min': float(np.min(prices)),
            'max': float(np.max(prices)),
            'total_value': float(np.sum(prices))
        }
