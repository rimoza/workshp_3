"""
Visualization functions for simulation results
Author: Ridwan
Course: Deep Learning for Cognitive Computing - Simulation Assignment 2
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def plot_throughput_time_distribution(results_df, save_path=None):
    """
    Plot distribution of throughput times across replications.
    
    Args:
        results_df: DataFrame with replication results
        save_path: Path to save figure (optional)
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogram
    axes[0].hist(results_df['mean_throughput_time'], bins=20, edgecolor='black', alpha=0.7)
    axes[0].axvline(results_df['mean_throughput_time'].mean(), 
                    color='red', linestyle='--', linewidth=2, label='Mean')
    axes[0].set_xlabel('Mean Throughput Time (minutes)')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Distribution of Mean Throughput Time Across Replications')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Box plot
    axes[1].boxplot([results_df['mean_throughput_time']], labels=['Throughput Time'])
    axes[1].set_ylabel('Time (minutes)')
    axes[1].set_title('Box Plot of Mean Throughput Time')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    plt.show()


def plot_blocking_metrics(results_df, save_path=None):
    """
    Plot blocking-related metrics.
    
    Args:
        results_df: DataFrame with replication results
        save_path: Path to save figure (optional)
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Blocking probability
    axes[0, 0].hist(results_df['blocking_probability'], bins=20, edgecolor='black', alpha=0.7, color='coral')
    axes[0, 0].axvline(results_df['blocking_probability'].mean(), 
                       color='red', linestyle='--', linewidth=2, label='Mean')
    axes[0, 0].set_xlabel('Blocking Probability')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].set_title('Distribution of Blocking Probability')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Theatre blocked fraction
    axes[0, 1].hist(results_df['theatre_blocked_fraction'], bins=20, edgecolor='black', alpha=0.7, color='lightblue')
    axes[0, 1].axvline(results_df['theatre_blocked_fraction'].mean(), 
                       color='red', linestyle='--', linewidth=2, label='Mean')
    axes[0, 1].set_xlabel('Theatre Blocked Fraction')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].set_title('Distribution of Theatre Blocked Time Fraction')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Number of blocking events
    axes[1, 0].hist(results_df['num_blocking_events'], bins=20, edgecolor='black', alpha=0.7, color='lightgreen')
    axes[1, 0].set_xlabel('Number of Blocking Events')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].set_title('Distribution of Blocking Events Count')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Scatter: Blocking probability vs Theatre utilization
    if 'mean_theatre_utilization' in results_df.columns:
        axes[1, 1].scatter(results_df['mean_theatre_utilization'], 
                          results_df['blocking_probability'], alpha=0.6)
        axes[1, 1].set_xlabel('Mean Theatre Utilization')
        axes[1, 1].set_ylabel('Blocking Probability')
        axes[1, 1].set_title('Blocking Probability vs Theatre Utilization')
        axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    plt.show()


def plot_queue_statistics(results_df, save_path=None):
    """
    Plot queue length statistics.
    
    Args:
        results_df: DataFrame with replication results
        save_path: Path to save figure (optional)
    """
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    queue_cols = ['mean_prep_queue', 'mean_theatre_queue', 'mean_recovery_queue']
    titles = ['Preparation Queue', 'Theatre Queue', 'Recovery Queue']
    colors = ['skyblue', 'lightcoral', 'lightgreen']
    
    for ax, col, title, color in zip(axes, queue_cols, titles, colors):
        if col in results_df.columns:
            ax.hist(results_df[col], bins=15, edgecolor='black', alpha=0.7, color=color)
            ax.axvline(results_df[col].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
            ax.set_xlabel('Mean Queue Length')
            ax.set_ylabel('Frequency')
            ax.set_title(f'{title} Length Distribution')
            ax.legend()
            ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    plt.show()


def plot_resource_utilization(results_df, save_path=None):
    """
    Plot resource utilization comparison.
    
    Args:
        results_df: DataFrame with replication results
        save_path: Path to save figure (optional)
    """
    util_cols = ['mean_prep_utilization', 'mean_theatre_utilization', 'mean_recovery_utilization']
    
    # Check which columns are available
    available_cols = [col for col in util_cols if col in results_df.columns]
    
    if not available_cols:
        print("No utilization data available")
        return
    
    # Prepare data
    util_data = []
    labels = []
    
    for col in available_cols:
        util_data.append(results_df[col].values)
        labels.append(col.replace('mean_', '').replace('_utilization', '').title())
    
    # Create box plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bp = ax.boxplot(util_data, labels=labels, patch_artist=True)
    
    # Color the boxes
    colors = ['skyblue', 'lightcoral', 'lightgreen']
    for patch, color in zip(bp['boxes'], colors[:len(bp['boxes'])]):
        patch.set_facecolor(color)
    
    ax.set_ylabel('Utilization')
    ax.set_title('Resource Utilization Comparison')
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim([0, 1])
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    plt.show()


def plot_sensitivity_analysis(sensitivity_results, parameter_name, metric_name='mean_throughput_time', save_path=None):
    """
    Plot sensitivity analysis results.
    
    Args:
        sensitivity_results: Dictionary from run_sensitivity_analysis
        parameter_name: Name of varied parameter
        metric_name: Metric to plot
        save_path: Path to save figure (optional)
    """
    param_values = []
    means = []
    ci_lowers = []
    ci_uppers = []
    
    for value, data in sorted(sensitivity_results.items()):
        summary = data['summary']
        if metric_name in summary:
            param_values.append(value)
            means.append(summary[metric_name]['mean'])
            ci_lowers.append(summary[metric_name]['ci_lower'])
            ci_uppers.append(summary[metric_name]['ci_upper'])
    
    if not param_values:
        print(f"No data available for metric: {metric_name}")
        return
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot mean with error bars
    ax.errorbar(param_values, means, 
                yerr=[np.array(means) - np.array(ci_lowers), 
                      np.array(ci_uppers) - np.array(means)],
                marker='o', capsize=5, capthick=2, linewidth=2, markersize=8)
    
    ax.set_xlabel(parameter_name.replace('_', ' ').title())
    ax.set_ylabel(metric_name.replace('_', ' ').title())
    ax.set_title(f'Sensitivity Analysis: {metric_name.replace("_", " ").title()}')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    plt.show()


def plot_comparison_bar_chart(comparison_results, metrics, save_path=None):
    """
    Create bar chart comparing multiple scenarios.
    
    Args:
        comparison_results: Dictionary from compare_scenarios
        metrics: List of metric names to compare
        save_path: Path to save figure (optional)
    """
    n_metrics = len(metrics)
    fig, axes = plt.subplots(1, n_metrics, figsize=(6*n_metrics, 5))
    
    if n_metrics == 1:
        axes = [axes]
    
    scenario_names = list(comparison_results.keys())
    
    for ax, metric in zip(axes, metrics):
        values = []
        errors = []
        
        for name in scenario_names:
            summary = comparison_results[name]['summary']
            if metric in summary:
                values.append(summary[metric]['mean'])
                # Error bar = confidence interval half-width
                ci_half = summary[metric]['ci_upper'] - summary[metric]['mean']
                errors.append(ci_half)
            else:
                values.append(0)
                errors.append(0)
        
        x_pos = np.arange(len(scenario_names))
        ax.bar(x_pos, values, yerr=errors, capsize=5, alpha=0.7, edgecolor='black')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(scenario_names, rotation=45, ha='right')
        ax.set_ylabel(metric.replace('_', ' ').title())
        ax.set_title(f'{metric.replace("_", " ").title()}')
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {save_path}")
    
    plt.show()


def create_all_plots(results_df, summary, output_dir='output/plots', interactive=False):
    """
    Create all standard plots and save them.

    Args:
        results_df: DataFrame with replication results
        summary: Summary dictionary
        output_dir: Directory to save plots
        interactive: If True, show interactive navigator instead of individual plots
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    print("\nGenerating visualizations...")

    if interactive:
        # Show interactive plot navigator
        show_interactive_plots(results_df, summary, output_dir)
    else:
        # 1. Throughput time
        plot_throughput_time_distribution(
            results_df,
            save_path=os.path.join(output_dir, 'throughput_time_distribution.png')
        )

        # 2. Blocking metrics
        plot_blocking_metrics(
            results_df,
            save_path=os.path.join(output_dir, 'blocking_metrics.png')
        )

        # 3. Queue statistics
        plot_queue_statistics(
            results_df,
            save_path=os.path.join(output_dir, 'queue_statistics.png')
        )

        # 4. Resource utilization
        plot_resource_utilization(
            results_df,
            save_path=os.path.join(output_dir, 'resource_utilization.png')
        )

    print(f"\nAll plots saved to: {output_dir}")


def show_interactive_plots(results_df, summary, output_dir='output/plots'):
    """
    Show all plots in an interactive window with navigation buttons.

    Args:
        results_df: DataFrame with replication results
        summary: Summary dictionary
        output_dir: Directory to save plots
    """

    class PlotNavigator:
        def __init__(self, results_df, output_dir):
            self.results_df = results_df
            self.output_dir = output_dir
            self.current_plot = 0
            self.plot_names = [
                'Throughput Time Distribution',
                'Blocking Metrics',
                'Queue Statistics',
                'Resource Utilization'
            ]

            # Create figure
            self.fig = plt.figure(figsize=(15, 9))

            # Main plot area
            self.ax_main = plt.axes([0.1, 0.15, 0.8, 0.75])

            # Navigation buttons
            ax_prev = plt.axes([0.25, 0.02, 0.15, 0.05])
            ax_next = plt.axes([0.6, 0.02, 0.15, 0.05])

            self.btn_prev = Button(ax_prev, '← Previous', color='lightblue', hovercolor='skyblue')
            self.btn_next = Button(ax_next, 'Next →', color='lightblue', hovercolor='skyblue')

            self.btn_prev.on_clicked(self.previous_plot)
            self.btn_next.on_clicked(self.next_plot)

            # Info text
            self.info_text = self.fig.text(0.5, 0.08, '', ha='center', fontsize=10)

            # Show first plot
            self.update_plot()

        def previous_plot(self, event):
            """Go to previous plot"""
            if self.current_plot > 0:
                self.current_plot -= 1
                self.update_plot()

        def next_plot(self, event):
            """Go to next plot"""
            if self.current_plot < len(self.plot_names) - 1:
                self.current_plot += 1
                self.update_plot()

        def update_plot(self):
            """Update the displayed plot"""
            # Clear the main axes
            self.ax_main.clear()

            # Remove any extra axes from previous plots
            for ax in self.fig.axes[3:]:  # Keep first 3 (main + 2 buttons)
                self.fig.delaxes(ax)

            # Create new subplot layout based on current plot
            if self.current_plot == 0:
                # Throughput Time Distribution (2 subplots)
                self.fig.clf()
                self._recreate_buttons()

                ax1 = self.fig.add_subplot(1, 2, 1)
                ax2 = self.fig.add_subplot(1, 2, 2)

                # Histogram
                ax1.hist(self.results_df['mean_throughput_time'], bins=20, edgecolor='black', alpha=0.7)
                ax1.axvline(self.results_df['mean_throughput_time'].mean(),
                           color='red', linestyle='--', linewidth=2, label='Mean')
                ax1.set_xlabel('Mean Throughput Time (minutes)')
                ax1.set_ylabel('Frequency')
                ax1.set_title('Distribution of Mean Throughput Time')
                ax1.legend()
                ax1.grid(True, alpha=0.3)

                # Box plot
                ax2.boxplot([self.results_df['mean_throughput_time']], labels=['Throughput Time'])
                ax2.set_ylabel('Time (minutes)')
                ax2.set_title('Box Plot')
                ax2.grid(True, alpha=0.3)

            elif self.current_plot == 1:
                # Blocking Metrics (4 subplots)
                self.fig.clf()
                self._recreate_buttons()

                axes = [self.fig.add_subplot(2, 2, i+1) for i in range(4)]

                # Blocking probability
                axes[0].hist(self.results_df['blocking_probability'], bins=20, edgecolor='black', alpha=0.7, color='coral')
                axes[0].axvline(self.results_df['blocking_probability'].mean(),
                               color='red', linestyle='--', linewidth=2, label='Mean')
                axes[0].set_xlabel('Blocking Probability')
                axes[0].set_ylabel('Frequency')
                axes[0].set_title('Blocking Probability Distribution')
                axes[0].legend()
                axes[0].grid(True, alpha=0.3)

                # Theatre blocked fraction
                axes[1].hist(self.results_df['theatre_blocked_fraction'], bins=20, edgecolor='black', alpha=0.7, color='lightblue')
                axes[1].axvline(self.results_df['theatre_blocked_fraction'].mean(),
                               color='red', linestyle='--', linewidth=2, label='Mean')
                axes[1].set_xlabel('Theatre Blocked Fraction')
                axes[1].set_ylabel('Frequency')
                axes[1].set_title('Theatre Blocked Time Fraction')
                axes[1].legend()
                axes[1].grid(True, alpha=0.3)

                # Number of blocking events
                axes[2].hist(self.results_df['num_blocking_events'], bins=20, edgecolor='black', alpha=0.7, color='lightgreen')
                axes[2].set_xlabel('Number of Blocking Events')
                axes[2].set_ylabel('Frequency')
                axes[2].set_title('Blocking Events Count')
                axes[2].grid(True, alpha=0.3)

                # Scatter: Blocking vs Utilization
                if 'mean_theatre_utilization' in self.results_df.columns:
                    axes[3].scatter(self.results_df['mean_theatre_utilization'],
                                  self.results_df['blocking_probability'], alpha=0.6)
                    axes[3].set_xlabel('Mean Theatre Utilization')
                    axes[3].set_ylabel('Blocking Probability')
                    axes[3].set_title('Blocking vs Theatre Utilization')
                    axes[3].grid(True, alpha=0.3)

            elif self.current_plot == 2:
                # Queue Statistics (3 subplots)
                self.fig.clf()
                self._recreate_buttons()

                axes = [self.fig.add_subplot(1, 3, i+1) for i in range(3)]

                queue_cols = ['mean_prep_queue', 'mean_theatre_queue', 'mean_recovery_queue']
                titles = ['Preparation Queue', 'Theatre Queue', 'Recovery Queue']
                colors = ['skyblue', 'lightcoral', 'lightgreen']

                for ax, col, title, color in zip(axes, queue_cols, titles, colors):
                    if col in self.results_df.columns:
                        ax.hist(self.results_df[col], bins=15, edgecolor='black', alpha=0.7, color=color)
                        ax.axvline(self.results_df[col].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
                        ax.set_xlabel('Mean Queue Length')
                        ax.set_ylabel('Frequency')
                        ax.set_title(f'{title} Distribution')
                        ax.legend()
                        ax.grid(True, alpha=0.3)

            elif self.current_plot == 3:
                # Resource Utilization (box plot)
                self.fig.clf()
                self._recreate_buttons()

                ax = self.fig.add_subplot(1, 1, 1)

                util_cols = ['mean_prep_utilization', 'mean_theatre_utilization', 'mean_recovery_utilization']
                available_cols = [col for col in util_cols if col in self.results_df.columns]

                if available_cols:
                    util_data = []
                    labels = []

                    for col in available_cols:
                        util_data.append(self.results_df[col].values)
                        labels.append(col.replace('mean_', '').replace('_utilization', '').title())

                    bp = ax.boxplot(util_data, labels=labels, patch_artist=True)

                    colors = ['skyblue', 'lightcoral', 'lightgreen']
                    for patch, color in zip(bp['boxes'], colors[:len(bp['boxes'])]):
                        patch.set_facecolor(color)

                    ax.set_ylabel('Utilization')
                    ax.set_title('Resource Utilization Comparison')
                    ax.grid(True, alpha=0.3, axis='y')
                    ax.set_ylim([0, 1])

            # Update info text
            self.info_text.set_text(f'Plot {self.current_plot + 1} of {len(self.plot_names)}: {self.plot_names[self.current_plot]}')

            # Update button states
            self.btn_prev.color = 'lightgray' if self.current_plot == 0 else 'lightblue'
            self.btn_prev.hovercolor = 'lightgray' if self.current_plot == 0 else 'skyblue'

            self.btn_next.color = 'lightgray' if self.current_plot == len(self.plot_names) - 1 else 'lightblue'
            self.btn_next.hovercolor = 'lightgray' if self.current_plot == len(self.plot_names) - 1 else 'skyblue'

            plt.tight_layout(rect=[0, 0.12, 1, 1])
            self.fig.canvas.draw()

        def _recreate_buttons(self):
            """Recreate navigation buttons after clearing figure"""
            ax_prev = plt.axes([0.25, 0.02, 0.15, 0.05])
            ax_next = plt.axes([0.6, 0.02, 0.15, 0.05])

            self.btn_prev = Button(ax_prev, '← Previous', color='lightblue', hovercolor='skyblue')
            self.btn_next = Button(ax_next, 'Next →', color='lightblue', hovercolor='skyblue')

            self.btn_prev.on_clicked(self.previous_plot)
            self.btn_next.on_clicked(self.next_plot)

            self.info_text = self.fig.text(0.5, 0.08, '', ha='center', fontsize=10)

        def show(self):
            """Display the navigator"""
            plt.show()

    # Create and show navigator
    navigator = PlotNavigator(results_df, output_dir)
    navigator.show()