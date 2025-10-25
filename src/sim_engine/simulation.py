"""
Core Simulation Engine Module
Generates random data points for property risk assessment.
"""
import numpy as np
from typing import Dict, List, Optional
from .config import SimulationConfig


class DataGenerator:
    """Generates random data for risk assessment simulation."""
    
    def __init__(self, config: SimulationConfig):
        """
        Initialize the data generator.
        
        Args:
            config: Simulation configuration
        """
        self.config = config
        self.rng = np.random.default_rng(config.random_seed)
    
    def generate_batch(self, batch_size: int) -> Dict[str, np.ndarray]:
        """
        Generate a batch of random risk data.
        
        Args:
            batch_size: Number of samples to generate
            
        Returns:
            Dictionary with hazard, vulnerability, and exposure arrays
        """
        hazard = self.rng.uniform(
            self.config.hazard_min,
            self.config.hazard_max,
            batch_size
        )
        
        vulnerability = self.rng.uniform(
            self.config.vulnerability_min,
            self.config.vulnerability_max,
            batch_size
        )
        
        exposure = self.rng.uniform(
            self.config.exposure_min,
            self.config.exposure_max,
            batch_size
        )
        
        return {
            'hazard': hazard,
            'vulnerability': vulnerability,
            'exposure': exposure
        }


class SimulationEngine:
    """Main simulation engine for property risk assessment."""
    
    def __init__(self, config: SimulationConfig):
        """
        Initialize the simulation engine.
        
        Args:
            config: Simulation configuration
        """
        self.config = config
        self.data_generator = DataGenerator(config)
    
    def run_simulation(self) -> Dict[str, np.ndarray]:
        """
        Run the full simulation and generate all data points.
        
        Returns:
            Dictionary containing all generated data
        """
        num_batches = (self.config.num_samples + self.config.batch_size - 1) // self.config.batch_size
        
        all_hazard = []
        all_vulnerability = []
        all_exposure = []
        
        for i in range(num_batches):
            # Calculate batch size (last batch might be smaller)
            remaining = self.config.num_samples - i * self.config.batch_size
            current_batch_size = min(self.config.batch_size, remaining)
            
            # Generate batch
            batch = self.data_generator.generate_batch(current_batch_size)
            
            all_hazard.append(batch['hazard'])
            all_vulnerability.append(batch['vulnerability'])
            all_exposure.append(batch['exposure'])
        
        # Combine all batches
        result = {
            'hazard': np.concatenate(all_hazard),
            'vulnerability': np.concatenate(all_vulnerability),
            'exposure': np.concatenate(all_exposure)
        }
        
        return result
    
    def generate_streaming(self, callback=None):
        """
        Generate data in streaming fashion for very large simulations.
        
        Args:
            callback: Optional callback function to process each batch
            
        Yields:
            Batches of generated data
        """
        num_batches = (self.config.num_samples + self.config.batch_size - 1) // self.config.batch_size
        
        for i in range(num_batches):
            remaining = self.config.num_samples - i * self.config.batch_size
            current_batch_size = min(self.config.batch_size, remaining)
            
            batch = self.data_generator.generate_batch(current_batch_size)
            
            if callback:
                callback(batch, i, num_batches)
            
            yield batch
