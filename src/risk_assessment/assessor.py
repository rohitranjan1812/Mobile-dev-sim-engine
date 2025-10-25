"""
Risk Assessment Module
Analyzes property risk based on hazard, vulnerability, and exposure factors.
"""
import numpy as np
from typing import Dict, Optional

try:
    from sim_engine.config import SimulationConfig
except ImportError:
    from ..sim_engine.config import SimulationConfig


class RiskAssessor:
    """Assesses property risk based on multiple factors."""
    
    def __init__(self, config: SimulationConfig):
        """
        Initialize the risk assessor.
        
        Args:
            config: Simulation configuration with risk weights
        """
        self.config = config
    
    def calculate_risk_score(
        self,
        hazard: np.ndarray,
        vulnerability: np.ndarray,
        exposure: np.ndarray
    ) -> np.ndarray:
        """
        Calculate composite risk score from individual factors.
        
        Args:
            hazard: Hazard values (0-1)
            vulnerability: Vulnerability values (0-1)
            exposure: Exposure values (0-1)
            
        Returns:
            Composite risk scores (0-1)
        """
        risk_score = (
            self.config.hazard_weight * hazard +
            self.config.vulnerability_weight * vulnerability +
            self.config.exposure_weight * exposure
        )
        return risk_score
    
    def assess_simulation_data(self, simulation_data: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """
        Assess risk for simulation data.
        
        Args:
            simulation_data: Dictionary with hazard, vulnerability, exposure arrays
            
        Returns:
            Dictionary with original data plus risk scores
        """
        risk_scores = self.calculate_risk_score(
            simulation_data['hazard'],
            simulation_data['vulnerability'],
            simulation_data['exposure']
        )
        
        result = simulation_data.copy()
        result['risk_score'] = risk_scores
        
        return result
    
    def categorize_risk(self, risk_scores: np.ndarray) -> np.ndarray:
        """
        Categorize risk scores into risk levels.
        
        Args:
            risk_scores: Array of risk scores (0-1)
            
        Returns:
            Array of risk categories (0=Low, 1=Medium, 2=High, 3=Very High)
        """
        categories = np.zeros(len(risk_scores), dtype=int)
        categories[risk_scores >= 0.25] = 1  # Medium
        categories[risk_scores >= 0.5] = 2   # High
        categories[risk_scores >= 0.75] = 3  # Very High
        return categories
    
    def get_risk_statistics(self, risk_scores: np.ndarray) -> Dict[str, float]:
        """
        Calculate statistics for risk scores.
        
        Args:
            risk_scores: Array of risk scores
            
        Returns:
            Dictionary with statistical measures
        """
        return {
            'mean': float(np.mean(risk_scores)),
            'median': float(np.median(risk_scores)),
            'std': float(np.std(risk_scores)),
            'min': float(np.min(risk_scores)),
            'max': float(np.max(risk_scores)),
            'percentile_25': float(np.percentile(risk_scores, 25)),
            'percentile_75': float(np.percentile(risk_scores, 75)),
            'percentile_90': float(np.percentile(risk_scores, 90)),
            'percentile_95': float(np.percentile(risk_scores, 95)),
            'percentile_99': float(np.percentile(risk_scores, 99))
        }
