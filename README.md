# Hospital Surgical Unit Simulation
![hospital-operating-room-doctors-surgery-room-surgery-operation-icon-hospital-operating-room-doctors-surgery-room-surgery-102016286](https://github.com/user-attachments/assets/3e06b868-44b5-40d9-9097-dc7507b4d2e6)

A discrete-event simulation of a hospital surgical unit using process-based modeling with blocking. This project simulates patient flow through preparation, operation, and recovery stages with limited resources and analyzes system performance under various configurations.

**Current Version**: Assignment 3 - Enhanced with pairwise comparisons, mixed patient types, and advanced statistical analysis.

## Overview

This simulation models a surgical unit where patients arrive, undergo preparation, surgery, and recovery. The system includes resource constraints and blocking mechanisms that realistically represent hospital operations. The simulation supports multiple replications, sensitivity analysis, and scenario comparison.

## Features

- **Process-based simulation** using SimPy
- **Blocking mechanisms** when resources are full
- **Multiple replications** for statistical confidence
- **Warmup period** to eliminate initialization bias
- **Comprehensive metrics** including throughput time, blocking probability, and resource utilization
- **Sensitivity analysis** for resource capacity optimization
- **Scenario comparison** for different operational conditions
- **Pairwise statistical comparisons** with identical random seeds
- **Mixed patient types** (regular vs. emergency) for realistic modeling
- **Advanced monitoring** including all-recovery-busy probability
- **Rich visualizations** with confidence intervals
- **Configurable parameters** for flexible experimentation

## Project Structure

```
workshop_3/
├── main.py                  # Main entry point for Assignment 3 simulation study
├── simulation_runner.py     # Core simulation execution, replication management, and pairwise comparisons
├── config.py               # Configuration parameters and scenario definitions (including Assignment 3 configs)
├── hospital_system.py      # Hospital system model with resources and processes
├── patient.py              # Patient entity class (supports mixed patient types)
├── results_analyzer.py     # Statistical analysis and metric calculation
├── visualizations.py       # Plotting and visualization functions
├── requirements.txt        # Python dependencies
├── output/                 # Output directory for results and plots
│   ├── assignment3_*.csv   # Assignment 3 results for each configuration
│   └── plots/
│       ├── baseline/       # Original Assignment 2 plots
│       ├── sensitivity/    # Sensitivity analysis plots
│       └── comparison/     # Scenario comparison plots
└── README.md
```

## System Model

### Patient Flow
1. **Arrival**: Patients arrive according to exponential interarrival times
2. **Preparation**: Patient undergoes preparation in a preparation room
3. **Operation**: Surgery is performed in an operating theatre
4. **Recovery**: Patient recovers in a recovery room
5. **Departure**: Patient leaves the system

### Process Flow Diagram
```
Patient Arrival → Preparation Room → Operating Theatre → Recovery Room → Departure
       ↓              ↓                    ↓ (Blocking)         ↓
   Generator      Request/Release      Request/Release    Request/Release
   Process        Resource Pool        Resource Pool      Resource Pool
```

**Sequence Diagram Reference:**
```
Patient Generator → Hospital System: Generate patient
Hospital System → Patient: Create patient process
Patient → Prep Pool: Request prep room
Prep Pool → Patient: Grant prep room
Patient → Patient: Preparation time
Patient → Prep Pool: Release prep room
Patient → Theatre: Request theatre
Theatre → Patient: Grant theatre
Patient → Patient: Operation time
Patient → Recovery Pool: Request recovery room
Recovery Pool → Patient: Recovery room full? (BLOCKING)
Patient → Theatre: Stay in theatre (blocked)
Recovery Pool → Patient: Grant recovery room
Patient → Theatre: Release theatre
Patient → Patient: Recovery time
Patient → Recovery Pool: Release recovery room
Patient → Hospital System: Departure
```

For a visual sequence diagram, see `docs/sequence_diagram.png` (to be added).

### Resources
- **Preparation Rooms**: Default 3 rooms
- **Operating Theatres**: Default 1 theatre
- **Recovery Rooms**: Default 3 rooms

### Blocking
- Patients are blocked from moving to the next stage if no resources are available
- Blocked patients occupy current resources until space becomes available
- System tracks blocking probability as a key performance metric

## Assignment 3 Enhancements

### New Features
- **Assignment 3 Configurations**: Three specific configurations (3P_4R, 3P_5R, 4P_5R)
- **Pairwise Comparisons**: Statistical comparison between configurations using identical random seeds
- **Mixed Patient Types**: Support for regular (20 min operations) and emergency (40 min operations) patients
- **Advanced Monitoring**: All-recovery-rooms-busy probability tracking
- **Statistical Significance Testing**: Confidence intervals for differences between configurations

### Assignment 3 Parameters
- **Simulation Duration**: 1000 time units per replication
- **Replications**: 20 independent runs per configuration
- **Warmup Period**: 200 time units
- **Patient Mix**: 80% regular patients, 20% emergency patients (personal twist)
- **Interarrival Adjustment**: Modified to maintain equivalent theatre utilization

### Key Metrics (Assignment 3 Focus)
- **Preparation Queue Length**: Average number of patients waiting for preparation
- **Blocking Probability**: Proportion of operations that experience blocking
- **All Recovery Busy Probability**: Frequency when all recovery rooms are occupied
- **Confidence Intervals**: 95% CIs for all metrics and differences

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```



## Usage

### Assignment 3: Complete Analysis (Recommended)

To run the Assignment 3 simulation study with all required analyses:

```bash
python main.py
```

This will execute:
1. **Configuration Analysis**: Run 3P_4R, 3P_5R, and 4P_5R configurations (20 replications each)
2. **Pairwise Comparisons**: Statistical comparison between configurations using identical seeds
3. **Personal Twist**: Compare original vs. mixed patient types (maintaining theatre utilization)
4. **Reference Baseline**: Run original Assignment 2 baseline for comparison
5. Save all results to `output/` directory

### Running Individual Assignment 3 Components

#### Configuration Analysis Only
```python
from config import ScenarioConfigs
from simulation_runner import run_simulation_study

# Run a specific Assignment 3 configuration
config = ScenarioConfigs.assignment3_3p4r()
results_df, summary, _ = run_simulation_study(config, verbose=True)
```

#### Pairwise Comparison
```python
from config import ScenarioConfigs
from simulation_runner import run_pairwise_comparison

# Compare two configurations with same seeds
config1 = ScenarioConfigs.assignment3_3p4r()
config2 = ScenarioConfigs.assignment3_3p5r()
results = run_pairwise_comparison(config1, config2, num_replications=20)
```

#### Personal Twist Analysis
```python
from config import ScenarioConfigs
from simulation_runner import run_pairwise_comparison

# Compare original vs. mixed patient types
original = ScenarioConfigs.assignment3_3p4r()
twist = ScenarioConfigs.assignment3_personal_twist()
results = run_pairwise_comparison(original, twist, num_replications=20)
```

### Running Individual Components

#### Baseline Scenario Only

```python
from config import ScenarioConfigs
from simulation_runner import run_simulation_study
from results_analyzer import print_aggregated_results

config = ScenarioConfigs.baseline()
results_df, summary, _ = run_simulation_study(config, verbose=True)
print_aggregated_results(summary)
```

#### Custom Scenario

```python
from config import SimulationConfig
from simulation_runner import run_simulation_study

# Create custom configuration
config = SimulationConfig()
config.num_prep_rooms = 4
config.num_operating_theatres = 2
config.num_recovery_rooms = 5
config.mean_interarrival = 20  # Increase patient arrival rate

# Run simulation
results_df, summary, _ = run_simulation_study(config, verbose=True)
```

#### Sensitivity Analysis

```python
from config import ScenarioConfigs
from simulation_runner import run_sensitivity_analysis

base_config = ScenarioConfigs.baseline()

# Analyze effect of operating theatre capacity
sensitivity_results = run_sensitivity_analysis(
    base_config,
    parameter_name='num_operating_theatres',
    parameter_values=[1, 2, 3],
    verbose=True
)
```

## Configuration Parameters

All parameters are configurable through the `SimulationConfig` class in `config.py`:

### Resource Capacities
- `num_prep_rooms`: Number of preparation rooms (default: 3)
- `num_operating_theatres`: Number of operating theatres (default: 1)
- `num_recovery_rooms`: Number of recovery rooms (default: 3)

### Time Parameters (minutes)
- `mean_interarrival`: Mean time between patient arrivals (default: 25)
- `mean_prep_time`: Mean preparation time (default: 40)
- `mean_operation_time`: Mean operation time (default: 20)
- `mean_recovery_time`: Mean recovery time (default: 40)

### Simulation Control
- `sim_duration`: Total simulation time in minutes (default: 24 * 60 = 1440)
- `warmup_period`: Warmup period in minutes (default: 8 * 60 = 480)
- `num_replications`: Number of independent replications (default: 30)
- `random_seed`: Base random seed for reproducibility (default: 42)
- `monitoring_interval`: Time between system state snapshots (default: 60)

## Performance Metrics

The simulation calculates the following metrics:

### Patient Flow Metrics
- **Mean Throughput Time**: Average total time in system (preparation + operation + recovery + waiting)
- **Mean Preparation Time**: Average time in preparation stage
- **Mean Operation Time**: Average time in operation stage
- **Mean Recovery Time**: Average time in recovery stage

### Resource Utilization
- **Mean Prep Room Utilization**: Average proportion of prep rooms in use
- **Mean Theatre Utilization**: Average proportion of theatres in use
- **Mean Recovery Room Utilization**: Average proportion of recovery rooms in use

### Blocking Metrics
- **Blocking Probability**: Proportion of times patients are blocked from progressing
- **Mean Blocking Time**: Average time patients spend blocked

### Assignment 3 Specific Metrics
- **Preparation Queue Length**: Average number of patients waiting for preparation rooms
- **All Recovery Busy Probability**: Proportion of monitoring intervals when all recovery rooms are occupied
- **Blocking State Probability**: Probability that the operating theatre is in a blocked state

### System Performance
- **Total Patients Arrived**: Total number of patient arrivals
- **Total Patients Departed**: Total number of patients who completed the process
- **Patients in System**: Current number of patients in the system

### Statistical Analysis (Assignment 3)
All metrics include:
- Mean across replications
- Standard deviation
- 95% confidence intervals (t-distribution based)
- Sample size (number of replications)
- **Pairwise Differences**: Confidence intervals for differences between configurations
- **Significance Testing**: Determination of statistically significant differences

## Output

### CSV Files
Results are saved to `output/` directory:
- `assignment3_3p_4r_results.csv`: Assignment 3 results for 3P_4R configuration
- `assignment3_3p_5r_results.csv`: Assignment 3 results for 3P_5R configuration
- `assignment3_4p_5r_results.csv`: Assignment 3 results for 4P_5R configuration
- `baseline_results.csv`: Original Assignment 2 baseline results (for reference)

### Plots
Visualizations are saved to `output/plots/`:

#### Baseline Plots (`output/plots/baseline/`)
- Throughput time distribution with histogram and KDE
- Resource utilization comparison
- Blocking probability analysis
- Confidence interval plots for all key metrics

#### Sensitivity Analysis (`output/plots/sensitivity/`)
- Throughput time vs. parameter value
- Blocking probability vs. parameter value
- Shows trend lines with confidence intervals

#### Scenario Comparison (`output/plots/comparison/`)
- Side-by-side bar charts comparing scenarios
- Multiple metrics in one plot
- Error bars showing confidence intervals

## Examples

### Example 1: Quick Baseline Run

```python
from config import ScenarioConfigs
from simulation_runner import run_simulation_study

# Run baseline with 10 replications (faster)
config = ScenarioConfigs.baseline()
config.num_replications = 10

results_df, summary, _ = run_simulation_study(config)
print(f"Mean throughput: {summary['mean_throughput_time']['mean']:.2f} minutes")
print(f"Blocking prob: {summary['blocking_probability']['mean']:.4f}")
```

### Example 2: Test Hospital Expansion

```python
from config import SimulationConfig
from simulation_runner import compare_scenarios

# Current configuration
current = SimulationConfig()
current.num_operating_theatres = 1
current.num_recovery_rooms = 3

# Proposed expansion
expanded = SimulationConfig()
expanded.num_operating_theatres = 2
expanded.num_recovery_rooms = 5

# Compare
results = compare_scenarios(
    [current, expanded],
    ['Current', 'Expanded'],
    verbose=True
)
```

### Example 3: Find Optimal Recovery Room Count

```python
from config import ScenarioConfigs
from simulation_runner import run_sensitivity_analysis

config = ScenarioConfigs.baseline()

results = run_sensitivity_analysis(
    config,
    'num_recovery_rooms',
    [1, 2, 3, 4, 5, 6, 7],
    verbose=True
)

# Find configuration with blocking < 0.01
for rooms, data in results.items():
    blocking = data['summary']['blocking_probability']['mean']
    if blocking < 0.01:
        print(f"Optimal: {rooms} recovery rooms (blocking: {blocking:.4f})")
        break
```

## Methodology

### Simulation Approach
- **Discrete-Event Simulation**: Time advances in discrete jumps as events occur
- **Process-Based Modeling**: Each patient is modeled as a process moving through stages
- **Blocking with Before-Service**: Patients occupy resources while blocked

### Statistical Considerations
- **Multiple Replications**: 30 independent runs for statistical reliability
- **Warmup Period**: 8-hour warmup to reach steady-state
- **Confidence Intervals**: 95% CIs using t-distribution
- **Seeded Random Numbers**: Reproducible results with configurable seeds

### Validation
- Patient conservation: Arrivals = Departures + In-system
- Utilization bounds: 0 <= utilization <= 1
- Blocking logic: Proper queue management and resource allocation

## Troubleshooting

### Common Issues

**Issue**: No results generated
- **Solution**: Check that warmup period is not too long for simulation duration
- Ensure at least some patients complete the system after warmup

**Issue**: High variance in results
- **Solution**: Increase number of replications
- Extend simulation duration
- Check for transient effects by adjusting warmup period

**Issue**: Unrealistic utilization values
- **Solution**: Verify service time parameters are reasonable
- Check resource capacity settings
- Ensure arrival rate matches system capacity

## Authors

- **Group Q** - Primary Developers

## Course Information

**Course**: Simulation - Assignment 3
**Institution**: University of Jyväskylä
**Date**: 2025

## Assignment 3 Requirements Met

✅ **Three Configurations**: 3P_4R, 3P_5R, 4P_5R with 20 replications of 1000 time units each
✅ **Key Metrics Monitoring**: Preparation queue length, blocking probability, all recovery busy probability
✅ **Statistical Analysis**: Point estimates, 95% confidence intervals, significance testing
✅ **Pairwise Comparisons**: Using identical random seeds for fair comparison
✅ **Personal Twist**: Mixed patient types (regular/emergency) with adjusted interarrival to maintain utilization
✅ **Advanced Analysis**: Confidence intervals for differences, significance determination

## License

This project is developed for academic purposes as part of coursework.

## Acknowledgments

- SimPy documentation and community
- Course instructors and teaching assistants
- Discrete-event simulation theory from course materials

## References

- Banks, J., Carson, J. S., Nelson, B. L., & Nicol, D. M. (2010). Discrete-Event System Simulation. Pearson.
- SimPy Documentation: https://simpy.readthedocs.io/
- Law, A. M., & Kelton, W. D. (2000). Simulation Modeling and Analysis. McGraw-Hill.

## Future Enhancements

Potential extensions to the simulation:
- Patient priority levels (emergency vs. scheduled)
- Staff resources (surgeons, nurses)
- Equipment failures and maintenance
- Different surgical procedure types with varying durations
- Real-time visualization of system state
- Optimization algorithms for resource allocation
- Cost analysis and budget constraints
- Patient rescheduling and cancellation policies

