"""
Interactive plot navigator for viewing multiple plots
Author: Ridwan
Course: Deep Learning for Cognitive Computing - Simulation Assignment 2
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np


class PlotNavigator:
    """Navigate through multiple plots using buttons"""

    def __init__(self, plot_functions, plot_args_list):
        """
        Initialize plot navigator

        Args:
            plot_functions: List of plotting functions
            plot_args_list: List of arguments for each plotting function
        """
        self.plot_functions = plot_functions
        self.plot_args_list = plot_args_list
        self.current_idx = 0
        self.fig = None

    def show(self):
        """Display the plot navigator"""
        self.fig = plt.figure(figsize=(14, 8))

        # Create axes for plot
        self.ax_plot = plt.axes([0.1, 0.2, 0.8, 0.7])

        # Create navigation buttons
        ax_prev = plt.axes([0.3, 0.05, 0.15, 0.075])
        ax_next = plt.axes([0.55, 0.05, 0.15, 0.075])

        self.btn_prev = Button(ax_prev, 'Previous')
        self.btn_next = Button(ax_next, 'Next')

        # Connect button events
        self.btn_prev.on_clicked(self.previous_plot)
        self.btn_next.on_clicked(self.next_plot)

        # Show first plot
        self._update_plot()

        plt.show()

    def previous_plot(self, event):
        """Show previous plot"""
        if self.current_idx > 0:
            self.current_idx -= 1
            self._update_plot()

    def next_plot(self, event):
        """Show next plot"""
        if self.current_idx < len(self.plot_functions) - 1:
            self.current_idx += 1
            self._update_plot()

    def _update_plot(self):
        """Update the displayed plot"""
        # Clear current plot
        self.ax_plot.clear()

        # Call the plotting function
        plt.sca(self.ax_plot)
        self.plot_functions[self.current_idx](**self.plot_args_list[self.current_idx])

        # Update title with index info
        current_title = self.ax_plot.get_title()
        self.ax_plot.set_title(f"{current_title}\n(Plot {self.current_idx + 1}/{len(self.plot_functions)})")

        # Update button states
        self.btn_prev.ax.set_visible(self.current_idx > 0)
        self.btn_next.ax.set_visible(self.current_idx < len(self.plot_functions) - 1)

        self.fig.canvas.draw()


def example_usage():
    """Example of how to use PlotNavigator"""
    import pandas as pd

    # Example: Create some dummy data
    data = pd.DataFrame({
        'mean_throughput_time': np.random.normal(100, 10, 30),
        'blocking_probability': np.random.uniform(0, 0.2, 30),
        'mean_theatre_utilization': np.random.uniform(0.6, 0.9, 30)
    })

    # Define plot functions
    def plot1(ax):
        ax.hist(data['mean_throughput_time'], bins=15, edgecolor='black')
        ax.set_title('Throughput Time Distribution')
        ax.set_xlabel('Time (minutes)')
        ax.set_ylabel('Frequency')

    def plot2(ax):
        ax.hist(data['blocking_probability'], bins=15, edgecolor='black', color='coral')
        ax.set_title('Blocking Probability Distribution')
        ax.set_xlabel('Probability')
        ax.set_ylabel('Frequency')

    def plot3(ax):
        ax.scatter(data['mean_theatre_utilization'], data['blocking_probability'])
        ax.set_title('Utilization vs Blocking')
        ax.set_xlabel('Theatre Utilization')
        ax.set_ylabel('Blocking Probability')

    # Create navigator
    plot_functions = [plot1, plot2, plot3]
    plot_args = [{'ax': None}, {'ax': None}, {'ax': None}]

    navigator = PlotNavigator(plot_functions, plot_args)
    navigator.show()


if __name__ == "__main__":
    example_usage()
