"""
Simulation Engine Configuration Module
Defines the configuration parameters for the simulation engine.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class SimulationConfig:
    """Configuration for property risk assessment simulation."""
    
    # Simulation parameters
    num_samples: int = 1000000
    batch_size: int = 10000
    random_seed: Optional[int] = None
    
    # Risk factor weights (must sum to 1.0)
    hazard_weight: float = 0.4
    vulnerability_weight: float = 0.3
    exposure_weight: float = 0.3
    
    # Risk factor ranges
    hazard_min: float = 0.0
    hazard_max: float = 1.0
    vulnerability_min: float = 0.0
    vulnerability_max: float = 1.0
    exposure_min: float = 0.0
    exposure_max: float = 1.0
    
    # Price optimization parameters
    base_property_price: float = 250000.0
    risk_penalty_factor: float = 0.5
    
    def __post_init__(self):
        """Validate configuration parameters."""
        # Validate weights sum to 1.0
        total_weight = self.hazard_weight + self.vulnerability_weight + self.exposure_weight
        if not (0.99 <= total_weight <= 1.01):  # Allow small floating point error
            raise ValueError(f"Risk factor weights must sum to 1.0, got {total_weight}")
        
        # Validate ranges
        if self.hazard_min >= self.hazard_max:
            raise ValueError("hazard_min must be less than hazard_max")
        if self.vulnerability_min >= self.vulnerability_max:
            raise ValueError("vulnerability_min must be less than vulnerability_max")
        if self.exposure_min >= self.exposure_max:
            raise ValueError("exposure_min must be less than exposure_max")
        
        # Validate positive values
        if self.num_samples <= 0:
            raise ValueError("num_samples must be positive")
        if self.batch_size <= 0:
            raise ValueError("batch_size must be positive")
        if self.base_property_price <= 0:
            raise ValueError("base_property_price must be positive")
