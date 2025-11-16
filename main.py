"""
Main entry point for hospital simulation study
Author: Ridwan
Course: Deep Learning for Cognitive Computing - Simulation Assignment 2
"""

import os
from config import SimulationConfig, ScenarioConfigs
from simulation_runner import run_simulation_study, run_sensitivity_analysis, compare_scenarios
from results_analyzer import print_aggregated_results
from visualizations import create_all_plots, plot_sensitivity_analysis, plot_comparison_bar_chart


def run_baseline_scenario():
    """Run baseline scenario"""
    print("\n" + "="*70)
    print("RUNNING BASELINE SCENARIO")
    print("="*70)
    
    config = ScenarioConfigs.baseline()
    config.print_config()
    
    results_df, summary, _ = run_simulation_study(config, verbose=True)
    
    # Print results
    print_aggregated_results(summary)
    
    # Save results
    os.makedirs('output', exist_ok=True)
    results_df.to_csv('output/baseline_results.csv', index=False)
    print("Results saved to: output/baseline_results.csv")
    
    # Create visualizations (set interactive=True to show navigation buttons)
    create_all_plots(results_df, summary, output_dir='output/plots/baseline', interactive=True)
    
    return results_df, summary


def run_recovery_sensitivity():
    """Run sensitivity analysis on recovery room capacity"""
    print("\n" + "="*70)
    print("RUNNING SENSITIVITY ANALYSIS: Recovery Room Capacity")
    print("="*70)
    
    base_config = ScenarioConfigs.baseline()
    
    sensitivity_results = run_sensitivity_analysis(
        base_config,
        parameter_name='num_recovery_rooms',
        parameter_values=[1, 2, 3, 4, 5],
        verbose=True
    )
    
    # Create plots
    os.makedirs('output/plots/sensitivity', exist_ok=True)
    
    plot_sensitivity_analysis(
        sensitivity_results,
        'num_recovery_rooms',
        'mean_throughput_time',
        save_path='output/plots/sensitivity/throughput_vs_recovery.png'
    )
    
    plot_sensitivity_analysis(
        sensitivity_results,
        'num_recovery_rooms',
        'blocking_probability',
        save_path='output/plots/sensitivity/blocking_vs_recovery.png'
    )
    
    # Print summary
    print("\n" + "="*70)
    print("SENSITIVITY ANALYSIS SUMMARY")
    print("="*70)
    print(f"\n{'Recovery Rooms':<15} {'Throughput Time':<20} {'Blocking Prob':<15}")
    print("-"*50)
    
    for value, data in sorted(sensitivity_results.items()):
        summary = data['summary']
        throughput = summary['mean_throughput_time']['mean']
        blocking = summary['blocking_probability']['mean']
        print(f"{value:<15} {throughput:<20.2f} {blocking:<15.4f}")
    
    return sensitivity_results


def run_scenario_comparison():
    """Compare different scenarios"""
    print("\n" + "="*70)
    print("RUNNING SCENARIO COMPARISON")
    print("="*70)
    
    scenarios = [
        ScenarioConfigs.baseline(),
        ScenarioConfigs.high_load(),
        ScenarioConfigs.low_load(),
    ]
    
    scenario_names = ['Baseline', 'High Load', 'Low Load']
    
    comparison_results = compare_scenarios(scenarios, scenario_names, verbose=True)
    
    # Create comparison plots
    os.makedirs('output/plots/comparison', exist_ok=True)
    
    plot_comparison_bar_chart(
        comparison_results,
        ['mean_throughput_time', 'blocking_probability', 'mean_theatre_utilization'],
        save_path='output/plots/comparison/scenario_comparison.png'
    )
    
    # Print comparison
    print("\n" + "="*70)
    print("SCENARIO COMPARISON SUMMARY")
    print("="*70)
    print(f"\n{'Scenario':<15} {'Throughput':<15} {'Blocking':<15} {'Theatre Util':<15}")
    print("-"*60)
    
    for name, data in comparison_results.items():
        summary = data['summary']
        throughput = summary['mean_throughput_time']['mean']
        blocking = summary['blocking_probability']['mean']
        util = summary['mean_theatre_utilization']['mean']
        print(f"{name:<15} {throughput:<15.2f} {blocking:<15.4f} {util:<15.4f}")
    
    return comparison_results


def main():
    """Main execution function"""
    print("\n" + "="*70)
    print("HOSPITAL SIMULATION STUDY")
    print("Process-Based Simulation with Blocking")
    print("Author: Ridwan")
    print("="*70)
    
    # Create output directories
    os.makedirs('output/plots', exist_ok=True)
    
    # Run baseline scenario
    print("\n[1/3] Running baseline scenario...")
    baseline_results, baseline_summary = run_baseline_scenario()
    
    # Run sensitivity analysis
    print("\n[2/3] Running sensitivity analysis...")
    sensitivity_results = run_recovery_sensitivity()
    
    # Run scenario comparison
    print("\n[3/3] Running scenario comparison...")
    comparison_results = run_scenario_comparison()
    
    # Final summary
    print("\n" + "="*70)
    print("SIMULATION STUDY COMPLETED")
    print("="*70)
    print("\nAll results saved to: output/")
    print("All plots saved to: output/plots/")
    print("\nKey findings:")
    print(f"  - Baseline mean throughput time: {baseline_summary['mean_throughput_time']['mean']:.2f} minutes")
    print(f"  - Baseline blocking probability: {baseline_summary['blocking_probability']['mean']:.4f}")
    print(f"  - Theatre utilization: {baseline_summary['mean_theatre_utilization']['mean']:.4f}")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
# ```

## File 8: `requirements.txt`
# ```
# simpy>=4.0.1
# numpy>=1.21.0
# pandas>=1.3.0
# matplotlib>=3.4.0
# seaborn>=0.11.0
# scipy>=1.7.0