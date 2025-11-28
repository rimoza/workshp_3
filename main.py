"""
Main entry point for hospital simulation study
Author: Ridwan
Course: Deep Learning for Cognitive Computing - Simulation Assignment 2
"""

import os
from config import SimulationConfig, ScenarioConfigs
from simulation_runner import run_simulation_study, run_sensitivity_analysis, compare_scenarios, run_pairwise_comparison
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


def run_assignment3_configurations():
    """Run Assignment 3: Three configurations (3p4r, 3p5r, 4p5r)"""
    print("\n" + "="*70)
    print("ASSIGNMENT 3: CONFIGURATION ANALYSIS")
    print("="*70)

    configs = [
        ScenarioConfigs.assignment3_3p4r(),
        ScenarioConfigs.assignment3_3p5r(),
        ScenarioConfigs.assignment3_4p5r()
    ]

    config_names = ['3P_4R', '3P_5R', '4P_5R']
    results = {}

    for config, name in zip(configs, config_names):
        print(f"\nRunning {name}...")
        config.print_config()

        results_df, summary, _ = run_simulation_study(config, verbose=True)
        results[name] = {'results_df': results_df, 'summary': summary, 'config': config}

        # Save results
        results_df.to_csv(f'output/assignment3_{name.lower()}_results.csv', index=False)

        # Print key metrics
        print(f"\n{name} Results:")
        print(f"  Mean Prep Queue Length: {summary['mean_prep_queue']['mean']:.4f}")
        print(f"  Blocking Probability: {summary['blocking_probability']['mean']:.4f}")
        print(f"  All Recovery Busy Prob: {summary['all_recovery_busy_probability']['mean']:.4f}")
        print(f"  Theatre Utilization: {summary['mean_theatre_utilization']['mean']:.4f}")

    return results


def run_assignment3_pairwise_comparisons():
    """Run Assignment 3: Pairwise comparisons with same seeds"""
    print("\n" + "="*70)
    print("ASSIGNMENT 3: PAIRWISE COMPARISONS")
    print("="*70)

    comparisons = [
        (ScenarioConfigs.assignment3_3p4r(), ScenarioConfigs.assignment3_3p5r(), '3P4R_vs_3P5R'),
        (ScenarioConfigs.assignment3_3p4r(), ScenarioConfigs.assignment3_4p5r(), '3P4R_vs_4P5R'),
        (ScenarioConfigs.assignment3_3p5r(), ScenarioConfigs.assignment3_4p5r(), '3P5R_vs_4P5R')
    ]

    results = {}

    for config1, config2, name in comparisons:
        print(f"\nRunning pairwise comparison: {name}...")

        pairwise_results = run_pairwise_comparison(config1, config2, num_replications=20, verbose=True)
        results[name] = pairwise_results

        # Print difference results
        diff_summary = pairwise_results['differences']['summary']
        print(f"\n{name} - Significant Differences (95% CI):")
        for metric in ['mean_prep_queue', 'blocking_probability', 'all_recovery_busy_probability']:
            if metric in diff_summary:
                mean_diff = diff_summary[metric]['mean']
                ci_lower = diff_summary[metric]['ci_lower']
                ci_upper = diff_summary[metric]['ci_upper']
                significant = ci_lower > 0 or ci_upper < 0
                print(f"  {metric}: {mean_diff:.4f} [{ci_lower:.4f}, {ci_upper:.4f}] {'***' if significant else ''}")

    return results


def run_assignment3_personal_twist():
    """Run Assignment 3: Personal twist comparison"""
    print("\n" + "="*70)
    print("ASSIGNMENT 3: PERSONAL TWIST - Mixed Patient Types")
    print("="*70)

    # Compare original 3p4r with personal twist
    config_original = ScenarioConfigs.assignment3_3p4r()
    config_twist = ScenarioConfigs.assignment3_personal_twist()

    print("\nOriginal Configuration (3P_4R):")
    config_original.print_config()

    print("\nPersonal Twist (Mixed Patient Types, adjusted interarrival):")
    config_twist.print_config()

    # Run comparison
    twist_results = run_pairwise_comparison(config_original, config_twist, num_replications=20, verbose=True)

    # Print comparison
    orig_summary = twist_results['config1']['summary']
    twist_summary = twist_results['config2']['summary']
    diff_summary = twist_results['differences']['summary']

    print("\n" + "="*70)
    print("PERSONAL TWIST COMPARISON RESULTS")
    print("="*70)
    print(f"\n{'Metric':<30} {'Original':>12} {'Twist':>12} {'Difference':>12}")
    print("-"*66)

    key_metrics = ['mean_theatre_utilization', 'blocking_probability', 'mean_prep_queue', 'all_recovery_busy_probability']
    for metric in key_metrics:
        if metric in orig_summary and metric in twist_summary:
            orig_val = orig_summary[metric]['mean']
            twist_val = twist_summary[metric]['mean']
            diff_val = diff_summary[metric]['mean'] if metric in diff_summary else 0
            print(f"{metric:<30} {orig_val:>12.4f} {twist_val:>12.4f} {diff_val:>12.4f}")

    return twist_results


def main():
    """Main execution function - Assignment 3"""
    print("\n" + "="*70)
    print("HOSPITAL SIMULATION STUDY - ASSIGNMENT 3")
    print("Process-Based Simulation with Blocking")
    print("Author: Ridwan")
    print("="*70)

    # Create output directories
    os.makedirs('output/plots', exist_ok=True)

    # Run Assignment 3 configurations
    print("\n[1/4] Running Assignment 3 configurations...")
    config_results = run_assignment3_configurations()

    # Run pairwise comparisons
    print("\n[2/4] Running pairwise comparisons...")
    pairwise_results = run_assignment3_pairwise_comparisons()

    # Run personal twist
    print("\n[3/4] Running personal twist analysis...")
    twist_results = run_assignment3_personal_twist()

    # Run original Assignment 2 for comparison (optional)
    print("\n[4/4] Running original Assignment 2 baseline for reference...")
    baseline_results, baseline_summary = run_baseline_scenario()

    # Final summary
    print("\n" + "="*70)
    print("ASSIGNMENT 3 SIMULATION STUDY COMPLETED")
    print("="*70)
    print("\nAll results saved to: output/")
    print("\nKey Assignment 3 findings:")
    for name, data in config_results.items():
        summary = data['summary']
        print(f"  {name}:")
        print(f"    Prep Queue: {summary['mean_prep_queue']['mean']:.4f}")
        print(f"    Blocking Prob: {summary['blocking_probability']['mean']:.4f}")
        print(f"    All Recovery Busy: {summary['all_recovery_busy_probability']['mean']:.4f}")
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