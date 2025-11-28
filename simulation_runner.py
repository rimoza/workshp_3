"""
Main simulation execution with multiple replications
Author: Group Q work
Course: Deep Learning for Cognitive Computing - Simulation Assignment 2
"""

import simpy
import random
import numpy as np
from patient import Patient
from hospital_system import HospitalSystem
from results_analyzer import SimulationResults, aggregate_replication_results
from config import SimulationConfig  # ADD THIS IMPORT


def run_single_replication(config, replication_id, verbose=False):
    """
    Run a single simulation replication.
    
    Args:
        config: SimulationConfig object
        replication_id: Integer ID for this replication
        verbose: Boolean, print progress if True
    
    Returns:
        dict: Metrics from this replication
    """
    # Set random seeds for reproducibility
    random.seed(config.random_seed + replication_id)
    np.random.seed(config.random_seed + replication_id)
    
    # Reset patient counter for each replication
    Patient.reset_counter()
    
    # Create SimPy environment
    env = simpy.Environment()
    
    # Create hospital system
    hospital = HospitalSystem(env, config)
    
    # Start processes
    env.process(hospital.patient_generator())
    env.process(hospital.monitoring_process())
    
    if verbose:
        print(f"  Starting replication {replication_id + 1}")
    
    # Run simulation
    env.run(until=config.sim_duration)
    
    if verbose:
        print(f"  Completed replication {replication_id + 1}")
        print(f"    Patients arrived: {hospital.total_patients_arrived}")
        print(f"    Patients departed: {hospital.total_patients_departed}")
        print(f"    Patients completed (after warmup): {len(hospital.patients_completed)}")
    
    # Analyze results
    results = SimulationResults(hospital)
    metrics = results.calculate_metrics()
    
    if metrics:
        metrics['replication_id'] = replication_id
    
    return metrics, hospital


def run_simulation_study(config, verbose=True, save_detailed=False):
    """
    Run multiple replications and aggregate results.
    
    Args:
        config: SimulationConfig object
        verbose: Boolean, print progress if True
        save_detailed: Boolean, save detailed patient data if True
    
    Returns:
        tuple: (results_df, summary, detailed_data)
    """
    if verbose:
        print(f"\nRunning simulation study with {config.num_replications} replications...")
        print(f"Scenario: {config.get_scenario_name()}\n")
    
    all_results = []
    all_hospital_data = []
    
    for rep in range(config.num_replications):
        if verbose and (rep + 1) % 5 == 0:
            print(f"Progress: {rep + 1}/{config.num_replications} replications completed")
        
        metrics, hospital = run_single_replication(config, rep, verbose=False)
        
        if metrics:
            all_results.append(metrics)
            
            if save_detailed:
                all_hospital_data.append(hospital)
    
    if verbose:
        print(f"Completed all {config.num_replications} replications\n")
    
    # Aggregate results
    results_df, summary = aggregate_replication_results(all_results)
    
    # Prepare detailed data if requested
    detailed_data = None
    if save_detailed and all_hospital_data:
        detailed_data = {
            'hospitals': all_hospital_data,
            'configs': config
        }
    
    return results_df, summary, detailed_data


def run_sensitivity_analysis(base_config, parameter_name, parameter_values, verbose=True):
    """
    Run sensitivity analysis by varying a parameter.
    
    Args:
        base_config: Base SimulationConfig object
        parameter_name: Name of parameter to vary (string)
        parameter_values: List of values to test
        verbose: Boolean, print progress if True
    
    Returns:
        dict: Results for each parameter value
    """
    sensitivity_results = {}
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"SENSITIVITY ANALYSIS: {parameter_name}")
        print(f"{'='*60}\n")
    
    for value in parameter_values:
        if verbose:
            print(f"\nTesting {parameter_name} = {value}...")
        
        # Create config for this scenario - use the import we added
        config = SimulationConfig()
        # Copy all attributes from base_config
        for key, val in base_config.__dict__.items():
            setattr(config, key, val)
        # Set the parameter we're varying
        setattr(config, parameter_name, value)
        
        # Run simulation study
        results_df, summary, _ = run_simulation_study(config, verbose=False)
        
        sensitivity_results[value] = {
            'results_df': results_df,
            'summary': summary,
            'config': config
        }
        
        if verbose and summary:
            print(f"  Mean throughput time: {summary['mean_throughput_time']['mean']:.2f}")
            print(f"  Blocking probability: {summary['blocking_probability']['mean']:.4f}")
    
    return sensitivity_results


def compare_scenarios(scenario_configs, scenario_names=None, verbose=True):
    """
    Compare multiple scenarios.
    
    Args:
        scenario_configs: List of SimulationConfig objects
        scenario_names: List of scenario names (optional)
        verbose: Boolean, print progress if True
    
    Returns:
        dict: Results for each scenario
    """
    if scenario_names is None:
        scenario_names = [f"Scenario {i+1}" for i in range(len(scenario_configs))]
    
    comparison_results = {}
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"SCENARIO COMPARISON")
        print(f"{'='*60}\n")
    
    for name, config in zip(scenario_names, scenario_configs):
        if verbose:
            print(f"\nRunning {name}...")
        
        results_df, summary, _ = run_simulation_study(config, verbose=False)
        
        comparison_results[name] = {
            'results_df': results_df,
            'summary': summary,
            'config': config
        }
    
    return comparison_results


def run_pairwise_comparison(config1, config2, num_replications=20, verbose=True):
    """
    Run pairwise comparison using the same random seeds for both configurations.

    Args:
        config1: First SimulationConfig object
        config2: Second SimulationConfig object
        num_replications: Number of replications
        verbose: Boolean, print progress if True

    Returns:
        dict: Results for both configurations and differences
    """
    if verbose:
        print(f"\n{'='*60}")
        print("PAIRWISE COMPARISON")
        print(f"Config 1: {config1.get_scenario_name()}")
        print(f"Config 2: {config2.get_scenario_name()}")
        print(f"Replications: {num_replications}")
        print(f"{'='*60}\n")

    results1 = []
    results2 = []
    differences = []

    for rep in range(num_replications):
        if verbose and (rep + 1) % 5 == 0:
            print(f"Progress: {rep + 1}/{num_replications} replications completed")

        # Run both configs with same seed
        seed = config1.random_seed + rep

        # Config 1
        config1_rep = config1.__class__()
        for key, val in config1.__dict__.items():
            setattr(config1_rep, key, val)
        config1_rep.random_seed = seed

        metrics1, _ = run_single_replication(config1_rep, rep, verbose=False)
        if metrics1:
            results1.append(metrics1)

        # Config 2
        config2_rep = config2.__class__()
        for key, val in config2.__dict__.items():
            setattr(config2_rep, key, val)
        config2_rep.random_seed = seed

        metrics2, _ = run_single_replication(config2_rep, rep, verbose=False)
        if metrics2:
            results2.append(metrics2)

        # Calculate differences
        if metrics1 and metrics2:
            diff = {}
            for key in metrics1.keys():
                if key in metrics2 and key != 'replication_id':
                    diff[key] = metrics1[key] - metrics2[key]
            diff['replication_id'] = rep
            differences.append(diff)

    # Aggregate results
    results_df1, summary1 = aggregate_replication_results(results1)
    results_df2, summary2 = aggregate_replication_results(results2)
    diff_df, diff_summary = aggregate_replication_results(differences)

    return {
        'config1': {'results_df': results_df1, 'summary': summary1, 'config': config1},
        'config2': {'results_df': results_df2, 'summary': summary2, 'config': config2},
        'differences': {'results_df': diff_df, 'summary': diff_summary}
    }