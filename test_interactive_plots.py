"""
Test script to demonstrate interactive plot navigation
Author: Group Q work
Course: Deep Learning for Cognitive Computing - Simulation Assignment 2
"""

import pandas as pd
import numpy as np
from visualizations import show_interactive_plots

# Generate sample data similar to simulation results
np.random.seed(42)
n_replications = 30

sample_data = pd.DataFrame({
    'replication_id': range(n_replications),
    'mean_throughput_time': np.random.normal(120, 15, n_replications),
    'blocking_probability': np.random.uniform(0.05, 0.25, n_replications),
    'theatre_blocked_fraction': np.random.uniform(0.1, 0.3, n_replications),
    'num_blocking_events': np.random.randint(5, 25, n_replications),
    'mean_prep_queue': np.random.uniform(0.5, 2.5, n_replications),
    'mean_theatre_queue': np.random.uniform(0.3, 1.5, n_replications),
    'mean_recovery_queue': np.random.uniform(1.0, 3.5, n_replications),
    'mean_prep_utilization': np.random.uniform(0.6, 0.85, n_replications),
    'mean_theatre_utilization': np.random.uniform(0.75, 0.95, n_replications),
    'mean_recovery_utilization': np.random.uniform(0.65, 0.90, n_replications),
})

print("="*70)
print("INTERACTIVE PLOT VIEWER TEST")
print("="*70)
print("\nThis will open an interactive plot window with navigation buttons.")
print("You should see:")
print("  - 'Previous' button (left)")
print("  - 'Next' button (right)")
print("  - Plot counter showing which plot you're viewing")
print("\nClick the buttons to navigate between different plots!")
print("="*70 + "\n")

# Show interactive plots
show_interactive_plots(sample_data, summary={})
