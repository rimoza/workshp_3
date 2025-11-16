"""
Configuration parameters for hospital simulation
Author: Group Q work
Course: Deep Learning for Cognitive Computing - Simulation Assignment 2
"""


class SimulationConfig:
    """
    Configuration class for hospital simulation parameters.
    All parameters are configurable to support different scenarios.
    """
    
    def __init__(self):
        # ============================================
        # Resource Capacities
        # ============================================
        self.num_prep_rooms = 3
        self.num_operating_theatres = 1
        self.num_recovery_rooms = 3
        
        # ============================================
        # Time Parameters (in minutes)
        # ============================================
        # Arrival process
        self.mean_interarrival = 25  # minutes
        
        # Service times
        self.mean_prep_time = 40      # minutes
        self.mean_operation_time = 20 # minutes
        self.mean_recovery_time = 40  # minutes
        
        # ============================================
        # Simulation Control Parameters
        # ============================================
        self.sim_duration = 24 * 60    # 24 hours in minutes
        self.warmup_period = 8 * 60    # 8 hours warmup period
        self.num_replications = 30     # Number of independent replications
        self.random_seed = 42          # Base random seed for reproducibility
        
        # Monitoring interval (minutes)
        self.monitoring_interval = 60  # Take snapshots every 60 minutes
        
        # ============================================
        # Distribution Types
        # ============================================
        # For future extension to different distributions
        self.interarrival_dist = 'exponential'
        self.prep_dist = 'exponential'
        self.operation_dist = 'exponential'
        self.recovery_dist = 'exponential'
        
    def get_scenario_name(self):
        """Generate a descriptive name for the current configuration"""
        return f"P{self.num_prep_rooms}_T{self.num_operating_theatres}_R{self.num_recovery_rooms}"
    
    def print_config(self):
        """Print configuration summary"""
        print("\n" + "="*60)
        print("SIMULATION CONFIGURATION")
        print("="*60)
        print(f"\nResource Configuration:")
        print(f"  Preparation Rooms:     {self.num_prep_rooms}")
        print(f"  Operating Theatres:    {self.num_operating_theatres}")
        print(f"  Recovery Rooms:        {self.num_recovery_rooms}")
        print(f"\nTime Parameters (minutes):")
        print(f"  Mean Interarrival:     {self.mean_interarrival}")
        print(f"  Mean Preparation:      {self.mean_prep_time}")
        print(f"  Mean Operation:        {self.mean_operation_time}")
        print(f"  Mean Recovery:         {self.mean_recovery_time}")
        print(f"\nSimulation Parameters:")
        print(f"  Total Duration:        {self.sim_duration} minutes ({self.sim_duration/60:.1f} hours)")
        print(f"  Warmup Period:         {self.warmup_period} minutes ({self.warmup_period/60:.1f} hours)")
        print(f"  Number of Replications: {self.num_replications}")
        print(f"  Random Seed:           {self.random_seed}")
        print("="*60 + "\n")


class ScenarioConfigs:
    """
    Predefined scenario configurations for experiments
    """
    
    @staticmethod
    def baseline():
        """Baseline scenario from assignment"""
        config = SimulationConfig()
        return config
    
    @staticmethod
    def sensitivity_recovery_1():
        """Sensitivity analysis: 1 recovery room"""
        config = SimulationConfig()
        config.num_recovery_rooms = 1
        return config
    
    @staticmethod
    def sensitivity_recovery_2():
        """Sensitivity analysis: 2 recovery rooms"""
        config = SimulationConfig()
        config.num_recovery_rooms = 2
        return config
    
    @staticmethod
    def sensitivity_recovery_4():
        """Sensitivity analysis: 4 recovery rooms"""
        config = SimulationConfig()
        config.num_recovery_rooms = 4
        return config
    
    @staticmethod
    def high_load():
        """High patient load scenario"""
        config = SimulationConfig()
        config.mean_interarrival = 15  # More patients
        return config
    
    @staticmethod
    def low_load():
        """Low patient load scenario"""
        config = SimulationConfig()
        config.mean_interarrival = 40  # Fewer patients
        return config