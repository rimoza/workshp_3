"""
Patient entity class
Author: Ridwan
Course: Deep Learning for Cognitive Computing - Simulation Assignment 2
"""

import random


class Patient:
    """
    Patient entity that flows through the hospital system.
    Each patient carries their individual service times for all phases.
    """
    
    # Class variable to track patient IDs
    patient_counter = 0
    
    def __init__(self, env, config):
        """
        Initialize a new patient with individual service times.
        
        Args:
            env: SimPy environment
            config: SimulationConfig object
        """
        # Assign unique ID
        Patient.patient_counter += 1
        self.id = Patient.patient_counter
        
        self.env = env
        
        # Generate individual service times using exponential distribution
        self.prep_time = random.expovariate(1.0 / config.mean_prep_time)
        self.operation_time = random.expovariate(1.0 / config.mean_operation_time)
        self.recovery_time = random.expovariate(1.0 / config.mean_recovery_time)
        
        # Initialize all timestamps to None
        self.arrival_time = env.now
        self.prep_start = None
        self.prep_end = None
        self.operation_start = None
        self.operation_end = None
        self.recovery_start = None
        self.recovery_end = None
        self.departure_time = None
        
        # Blocking tracking
        self.was_blocked = False
        self.blocking_start = None
        self.blocking_end = None
        self.blocking_duration = 0
        
        # Waiting times
        self.wait_for_prep = None
        self.wait_for_operation = None
        self.wait_for_recovery = None
        
    def calculate_times(self):
        """Calculate derived time metrics"""
        if self.departure_time is not None:
            # Total time in system
            self.total_time = self.departure_time - self.arrival_time
            
            # Waiting times
            if self.prep_start is not None:
                self.wait_for_prep = self.prep_start - self.arrival_time
            
            if self.operation_start is not None and self.prep_end is not None:
                self.wait_for_operation = self.operation_start - self.prep_end
            
            if self.recovery_start is not None and self.operation_end is not None:
                self.wait_for_recovery = self.recovery_start - self.operation_end
                
    def to_dict(self):
        """Convert patient data to dictionary for analysis"""
        self.calculate_times()
        
        return {
            'patient_id': self.id,
            'arrival_time': self.arrival_time,
            'prep_start': self.prep_start,
            'prep_end': self.prep_end,
            'operation_start': self.operation_start,
            'operation_end': self.operation_end,
            'recovery_start': self.recovery_start,
            'recovery_end': self.recovery_end,
            'departure_time': self.departure_time,
            'total_time': self.total_time if hasattr(self, 'total_time') else None,
            'wait_for_prep': self.wait_for_prep,
            'wait_for_operation': self.wait_for_operation,
            'wait_for_recovery': self.wait_for_recovery,
            'was_blocked': self.was_blocked,
            'blocking_duration': self.blocking_duration,
            'prep_time': self.prep_time,
            'operation_time': self.operation_time,
            'recovery_time': self.recovery_time
        }
    
    def __repr__(self):
        return f"Patient({self.id})"
    
    @classmethod
    def reset_counter(cls):
        """Reset the patient counter (useful for new replications)"""
        cls.patient_counter = 0