"""
Hospital system with resource pools and patient processes
Author: Group Q work
Course: Deep Learning for Cognitive Computing - Simulation Assignment 2
"""

import simpy
import random


class HospitalSystem:
    """
    Main hospital simulation system with resource pools and patient flow.
    Implements process-based simulation with blocking mechanism.
    """
    
    def __init__(self, env, config):
        """
        Initialize hospital system with resources.
        
        Args:
            env: SimPy environment
            config: SimulationConfig object
        """
        self.env = env
        self.config = config
        
        # ============================================
        # Create Resource Pools
        # ============================================
        self.prep_pool = simpy.Resource(env, capacity=config.num_prep_rooms)
        self.theatre = simpy.Resource(env, capacity=config.num_operating_theatres)
        self.recovery_pool = simpy.Resource(env, capacity=config.num_recovery_rooms)
        
        # ============================================
        # Data Collection
        # ============================================
        # Completed patients (after warmup)
        self.patients_completed = []
        
        # Blocking statistics
        self.theatre_blocked_time = 0
        self.blocking_events_count = 0
        
        # Time series data for monitoring
        self.prep_queue_data = []
        self.theatre_queue_data = []
        self.recovery_queue_data = []
        self.theatre_utilization_data = []
        
        # For tracking current state
        self.total_patients_arrived = 0
        self.total_patients_departed = 0
        
    def patient_process(self, patient):
        """
        Main patient lifecycle process.
        Patient flows through: Preparation -> Operation -> Recovery
        
        Key feature: Theatre blocking when recovery is full
        
        Args:
            patient: Patient object
        """
        
        # ============================================
        # PHASE 1: PREPARATION
        # ============================================
        prep_request = self.prep_pool.request()
        yield prep_request
        
        patient.prep_start = self.env.now
        yield self.env.timeout(patient.prep_time)
        patient.prep_end = self.env.now
        
        self.prep_pool.release(prep_request)
        
        # ============================================
        # PHASE 2: OPERATION
        # ============================================
        theatre_request = self.theatre.request()
        yield theatre_request
        
        patient.operation_start = self.env.now
        yield self.env.timeout(patient.operation_time)
        patient.operation_end = self.env.now
        
        # ============================================
        # CRITICAL SECTION: Blocking Mechanism
        # ============================================
        # After operation completes, patient needs recovery bed
        # If no recovery bed available, patient stays in theatre (BLOCKING)
        
        recovery_request = self.recovery_pool.request()
        
        # Check if recovery pool is full
        if self.recovery_pool.count >= self.recovery_pool.capacity:
            # Theatre is blocked - patient cannot leave
            patient.was_blocked = True
            patient.blocking_start = self.env.now
            self.blocking_events_count += 1
        
        # Wait for recovery bed (theatre stays occupied if blocking)
        yield recovery_request
        
        # Recovery bed obtained
        if patient.was_blocked:
            patient.blocking_end = self.env.now
            patient.blocking_duration = patient.blocking_end - patient.blocking_start
            self.theatre_blocked_time += patient.blocking_duration
        
        patient.recovery_start = self.env.now
        
        # Now release theatre - patient has moved to recovery
        self.theatre.release(theatre_request)
        
        # ============================================
        # PHASE 3: RECOVERY
        # ============================================
        yield self.env.timeout(patient.recovery_time)
        patient.recovery_end = self.env.now
        
        # Release recovery bed
        self.recovery_pool.release(recovery_request)
        
        # ============================================
        # DEPARTURE
        # ============================================
        patient.departure_time = self.env.now
        self.total_patients_departed += 1
        
        # Only collect statistics after warmup period
        if self.env.now > self.config.warmup_period:
            self.patients_completed.append(patient)
    
    def patient_generator(self):
        """
        Generate patient arrivals according to arrival process.
        Uses exponential interarrival times (Poisson process).
        """
        while True:
            # Generate interarrival time
            interarrival = random.expovariate(1.0 / self.config.mean_interarrival)
            yield self.env.timeout(interarrival)
            
            # Create new patient
            from patient import Patient
            patient = Patient(self.env, self.config)
            self.total_patients_arrived += 1
            
            # Start patient process
            self.env.process(self.patient_process(patient))
    
    def monitoring_process(self):
        """
        Monitor system state at regular intervals.
        Collects queue lengths and resource utilization.
        """
        while True:
            yield self.env.timeout(self.config.monitoring_interval)
            
            # Only collect data after warmup period
            if self.env.now > self.config.warmup_period:
                # Preparation queue
                self.prep_queue_data.append({
                    'time': self.env.now,
                    'queue_length': len(self.prep_pool.queue),
                    'in_service': self.prep_pool.count,
                    'utilization': self.prep_pool.count / self.prep_pool.capacity
                })
                
                # Theatre queue
                self.theatre_queue_data.append({
                    'time': self.env.now,
                    'queue_length': len(self.theatre.queue),
                    'in_service': self.theatre.count,
                    'utilization': self.theatre.count / self.theatre.capacity
                })
                
                # Recovery queue
                self.recovery_queue_data.append({
                    'time': self.env.now,
                    'queue_length': len(self.recovery_pool.queue),
                    'in_service': self.recovery_pool.count,
                    'utilization': self.recovery_pool.count / self.recovery_pool.capacity
                })
    
    def get_current_state(self):
        """Get current system state snapshot"""
        return {
            'time': self.env.now,
            'total_arrived': self.total_patients_arrived,
            'total_departed': self.total_patients_departed,
            'in_system': self.total_patients_arrived - self.total_patients_departed,
            'prep_queue': len(self.prep_pool.queue),
            'prep_busy': self.prep_pool.count,
            'theatre_queue': len(self.theatre.queue),
            'theatre_busy': self.theatre.count,
            'recovery_queue': len(self.recovery_pool.queue),
            'recovery_busy': self.recovery_pool.count
        }