"""
Analysis and reporting of simulation results
Author: Group Q work
Course: Deep Learning for Cognitive Computing - Simulation Assignment 2
"""

import numpy as np
import pandas as pd
from scipy import stats


class SimulationResults:
    """
    Analyze and report simulation results.
    Calculates key performance metrics and generates reports.
    """
    
    def __init__(self, hospital):
        """
        Initialize results analyzer.
        
        Args:
            hospital: HospitalSystem object with completed simulation
        """
        self.hospital = hospital
        self.config = hospital.config
        self.metrics = None
        
    def calculate_metrics(self):
        """
        Calculate all key performance metrics.
        
        Returns:
            dict: Dictionary of calculated metrics
        """
        patients = self.hospital.patients_completed
        
        if not patients:
            return None
        
        # Calculate all patient metrics
        for patient in patients:
            patient.calculate_times()
        
        metrics = {}
        
        # ============================================
        # Primary Metrics
        # ============================================
        
        # 1. Average Throughput Time
        throughput_times = [p.total_time for p in patients if p.total_time is not None]
        if throughput_times:
            metrics['mean_throughput_time'] = np.mean(throughput_times)
            metrics['std_throughput_time'] = np.std(throughput_times)
            metrics['median_throughput_time'] = np.median(throughput_times)
            metrics['min_throughput_time'] = np.min(throughput_times)
            metrics['max_throughput_time'] = np.max(throughput_times)
        
        # 2. Blocking Probability (Event-based)
        total_operations = len(patients)
        blocked_operations = sum(1 for p in patients if p.was_blocked)
        metrics['blocking_probability'] = blocked_operations / total_operations if total_operations > 0 else 0
        metrics['num_blocking_events'] = blocked_operations
        
        # 3. Theatre Blocked Time (Time-based)
        sim_time = self.config.sim_duration - self.config.warmup_period
        metrics['theatre_blocked_time'] = self.hospital.theatre_blocked_time
        metrics['theatre_blocked_fraction'] = self.hospital.theatre_blocked_time / sim_time if sim_time > 0 else 0

        # 4. All Recovery Rooms Busy Probability (Assignment 3)
        if self.hospital.monitoring_intervals_count > 0:
            metrics['all_recovery_busy_probability'] = self.hospital.all_recovery_busy_count / self.hospital.monitoring_intervals_count
        else:
            metrics['all_recovery_busy_probability'] = 0
        
        # 4. Patient counts
        metrics['num_patients_completed'] = total_operations
        metrics['num_patients_arrived'] = self.hospital.total_patients_arrived
        
        # ============================================
        # Waiting Time Metrics
        # ============================================
        wait_prep = [p.wait_for_prep for p in patients if p.wait_for_prep is not None]
        wait_operation = [p.wait_for_operation for p in patients if p.wait_for_operation is not None]
        wait_recovery = [p.wait_for_recovery for p in patients if p.wait_for_recovery is not None]
        
        if wait_prep:
            metrics['mean_wait_prep'] = np.mean(wait_prep)
            metrics['max_wait_prep'] = np.max(wait_prep)
        
        if wait_operation:
            metrics['mean_wait_operation'] = np.mean(wait_operation)
            metrics['max_wait_operation'] = np.max(wait_operation)
        
        if wait_recovery:
            metrics['mean_wait_recovery'] = np.mean(wait_recovery)
            metrics['max_wait_recovery'] = np.max(wait_recovery)
        
        # ============================================
        # Queue Statistics
        # ============================================
        if self.hospital.prep_queue_data:
            prep_df = pd.DataFrame(self.hospital.prep_queue_data)
            metrics['mean_prep_queue'] = prep_df['queue_length'].mean()
            metrics['max_prep_queue'] = prep_df['queue_length'].max()
            metrics['mean_prep_utilization'] = prep_df['utilization'].mean()
        
        if self.hospital.theatre_queue_data:
            theatre_df = pd.DataFrame(self.hospital.theatre_queue_data)
            metrics['mean_theatre_queue'] = theatre_df['queue_length'].mean()
            metrics['max_theatre_queue'] = theatre_df['queue_length'].max()
            metrics['mean_theatre_utilization'] = theatre_df['utilization'].mean()
        
        if self.hospital.recovery_queue_data:
            recovery_df = pd.DataFrame(self.hospital.recovery_queue_data)
            metrics['mean_recovery_queue'] = recovery_df['queue_length'].mean()
            metrics['max_recovery_queue'] = recovery_df['queue_length'].max()
            metrics['mean_recovery_utilization'] = recovery_df['utilization'].mean()
        
        # ============================================
        # Blocking Duration Statistics
        # ============================================
        blocking_durations = [p.blocking_duration for p in patients if p.was_blocked]
        if blocking_durations:
            metrics['mean_blocking_duration'] = np.mean(blocking_durations)
            metrics['max_blocking_duration'] = np.max(blocking_durations)
        
        self.metrics = metrics
        return metrics
    
    def get_patient_dataframe(self):
        """
        Get detailed patient data as DataFrame.
        
        Returns:
            pandas.DataFrame: Patient-level data
        """
        if not self.hospital.patients_completed:
            return None
        
        patient_data = [p.to_dict() for p in self.hospital.patients_completed]
        return pd.DataFrame(patient_data)
    
    def print_summary(self, metrics=None):
        """
        Print formatted summary of results.
        
        Args:
            metrics: dict of metrics (if None, uses self.metrics)
        """
        if metrics is None:
            metrics = self.metrics
        
        if metrics is None:
            print("No metrics available. Run calculate_metrics() first.")
            return
        
        print("\n" + "="*70)
        print("SIMULATION RESULTS SUMMARY")
        print("="*70)
        
        print(f"\nPatients:")
        print(f"  Completed: {metrics.get('num_patients_completed', 0)}")
        
        print(f"\nThroughput Time (minutes):")
        print(f"  Mean:   {metrics.get('mean_throughput_time', 0):.2f}")
        print(f"  Std:    {metrics.get('std_throughput_time', 0):.2f}")
        print(f"  Median: {metrics.get('median_throughput_time', 0):.2f}")
        print(f"  Min:    {metrics.get('min_throughput_time', 0):.2f}")
        print(f"  Max:    {metrics.get('max_throughput_time', 0):.2f}")
        
        print(f"\nBlocking Statistics:")
        print(f"  Blocking Probability: {metrics.get('blocking_probability', 0):.4f} ({metrics.get('blocking_probability', 0)*100:.2f}%)")
        print(f"  Number of Blocking Events: {metrics.get('num_blocking_events', 0)}")
        print(f"  Theatre Blocked Fraction: {metrics.get('theatre_blocked_fraction', 0):.4f} ({metrics.get('theatre_blocked_fraction', 0)*100:.2f}%)")
        print(f"  Total Theatre Blocked Time: {metrics.get('theatre_blocked_time', 0):.2f} minutes")
        if 'mean_blocking_duration' in metrics:
            print(f"  Mean Blocking Duration: {metrics.get('mean_blocking_duration', 0):.2f} minutes")
        
        print(f"\nQueue Lengths (Average):")
        print(f"  Preparation:  {metrics.get('mean_prep_queue', 0):.2f}")
        print(f"  Theatre:      {metrics.get('mean_theatre_queue', 0):.2f}")
        print(f"  Recovery:     {metrics.get('mean_recovery_queue', 0):.2f}")
        
        print(f"\nResource Utilization:")
        print(f"  Preparation:  {metrics.get('mean_prep_utilization', 0):.4f} ({metrics.get('mean_prep_utilization', 0)*100:.2f}%)")
        print(f"  Theatre:      {metrics.get('mean_theatre_utilization', 0):.4f} ({metrics.get('mean_theatre_utilization', 0)*100:.2f}%)")
        print(f"  Recovery:     {metrics.get('mean_recovery_utilization', 0):.4f} ({metrics.get('mean_recovery_utilization', 0)*100:.2f}%)")
        
        print(f"\nWaiting Times (minutes):")
        if 'mean_wait_prep' in metrics:
            print(f"  For Preparation: {metrics.get('mean_wait_prep', 0):.2f}")
        if 'mean_wait_operation' in metrics:
            print(f"  For Operation:   {metrics.get('mean_wait_operation', 0):.2f}")
        if 'mean_wait_recovery' in metrics:
            print(f"  For Recovery:    {metrics.get('mean_wait_recovery', 0):.2f}")
        
        print("="*70 + "\n")


def aggregate_replication_results(all_results_list):
    """
    Aggregate results from multiple replications and calculate confidence intervals.
    
    Args:
        all_results_list: List of metrics dictionaries from each replication
    
    Returns:
        tuple: (results_df, summary_dict)
    """
    if not all_results_list:
        return None, None
    
    # Convert to DataFrame
    results_df = pd.DataFrame(all_results_list)
    
    # Calculate summary statistics with 95% confidence intervals
    summary = {}
    
    for col in results_df.columns:
        if col != 'replication_id':
            data = results_df[col].dropna()
            
            if len(data) > 0:
                mean = data.mean()
                std = data.std()
                n = len(data)
                
                # Calculate 95% confidence interval
                confidence = 0.95
                degrees_freedom = n - 1
                t_critical = stats.t.ppf((1 + confidence) / 2, degrees_freedom)
                margin_error = t_critical * (std / np.sqrt(n))
                
                summary[col] = {
                    'mean': mean,
                    'std': std,
                    'min': data.min(),
                    'max': data.max(),
                    'median': data.median(),
                    'ci_lower': mean - margin_error,
                    'ci_upper': mean + margin_error,
                    'n': n
                }
    
    return results_df, summary


def print_aggregated_results(summary):
    """
    Print aggregated results from multiple replications.
    
    Args:
        summary: Summary dictionary from aggregate_replication_results
    """
    print("\n" + "="*80)
    print("AGGREGATED RESULTS FROM MULTIPLE REPLICATIONS")
    print("="*80)
    
    # Key metrics to highlight
    key_metrics = [
        'mean_throughput_time',
        'blocking_probability',
        'theatre_blocked_fraction',
        'mean_theatre_queue',
        'mean_theatre_utilization'
    ]
    
    print(f"\n{'Metric':<35} {'Mean':>10} {'Std':>10} {'95% CI':>25}")
    print("-"*80)
    
    for metric in key_metrics:
        if metric in summary:
            stats = summary[metric]
            ci_str = f"[{stats['ci_lower']:.4f}, {stats['ci_upper']:.4f}]"
            print(f"{metric:<35} {stats['mean']:>10.4f} {stats['std']:>10.4f} {ci_str:>25}")
    
    print("\n" + "="*80 + "\n")