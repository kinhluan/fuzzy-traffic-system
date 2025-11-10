"""
Fuzzy Membership Functions for Traffic Control System

Defines membership functions for:
- Vehicle density (Low, Medium, High)
- Waiting time (Short, Medium, Long, Very Long)
- Green light duration (Short, Medium, Long)
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from typing import Dict, Tuple


def create_membership_functions() -> Tuple[Dict[str, ctrl.Antecedent], ctrl.Consequent]:
    """
    Create all fuzzy membership functions for the traffic control system.

    Returns:
        Tuple containing:
        - Dictionary of antecedent (input) variables
        - Consequent (output) variable for green time
    """

    # Input Variables (Antecedents)
    # Vehicle density for each direction (0-100 vehicles)
    density_north = ctrl.Antecedent(np.arange(0, 101, 1), 'density_north')
    density_south = ctrl.Antecedent(np.arange(0, 101, 1), 'density_south')
    density_east = ctrl.Antecedent(np.arange(0, 101, 1), 'density_east')
    density_west = ctrl.Antecedent(np.arange(0, 101, 1), 'density_west')

    # Waiting time for each direction (0-300 seconds)
    waiting_north = ctrl.Antecedent(np.arange(0, 301, 1), 'waiting_north')
    waiting_south = ctrl.Antecedent(np.arange(0, 301, 1), 'waiting_south')
    waiting_east = ctrl.Antecedent(np.arange(0, 301, 1), 'waiting_east')
    waiting_west = ctrl.Antecedent(np.arange(0, 301, 1), 'waiting_west')

    # Output Variable (Consequent)
    # Green light duration (10-90 seconds)
    green_time = ctrl.Consequent(np.arange(10, 91, 1), 'green_time')

    # Define membership functions for vehicle density
    # Low: 0-50, Medium: 20-80, High: 50-100
    for density in [density_north, density_south, density_east, density_west]:
        density['low'] = fuzz.trimf(density.universe, [0, 0, 50])
        density['medium'] = fuzz.trimf(density.universe, [20, 50, 80])
        density['high'] = fuzz.trimf(density.universe, [50, 100, 100])

    # Define membership functions for waiting time
    # Short: 0-60s, Medium: 40-120s, Long: 100-200s, Very Long: 180-300s
    for waiting in [waiting_north, waiting_south, waiting_east, waiting_west]:
        waiting['short'] = fuzz.trimf(waiting.universe, [0, 0, 60])
        waiting['medium'] = fuzz.trimf(waiting.universe, [40, 100, 160])
        waiting['long'] = fuzz.trimf(waiting.universe, [120, 200, 280])
        waiting['very_long'] = fuzz.trimf(waiting.universe, [240, 300, 300])

    # Define membership functions for green time output
    # Short: 10-30s, Medium: 25-55s, Long: 50-70s, Very Long: 65-90s
    green_time['short'] = fuzz.trimf(green_time.universe, [10, 10, 30])
    green_time['medium'] = fuzz.trimf(green_time.universe, [25, 40, 55])
    green_time['long'] = fuzz.trimf(green_time.universe, [50, 60, 70])
    green_time['very_long'] = fuzz.trimf(green_time.universe, [65, 90, 90])

    # Collect all antecedents
    antecedents = {
        'density_north': density_north,
        'density_south': density_south,
        'density_east': density_east,
        'density_west': density_west,
        'waiting_north': waiting_north,
        'waiting_south': waiting_south,
        'waiting_east': waiting_east,
        'waiting_west': waiting_west,
    }

    return antecedents, green_time


def visualize_membership_functions(antecedents: Dict[str, ctrl.Antecedent],
                                   consequent: ctrl.Consequent,
                                   save_path: str = None):
    """
    Visualize membership functions for documentation and analysis.

    Args:
        antecedents: Dictionary of input variables
        consequent: Output variable
        save_path: Optional path to save the visualization
    """
    import matplotlib.pyplot as plt

    # Visualize density membership functions
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Fuzzy Membership Functions', fontsize=16, fontweight='bold')

    # Plot density (one example - North)
    ax = axes[0, 0]
    density_north = antecedents['density_north']
    for term in density_north.terms:
        ax.plot(density_north.universe,
               density_north[term].mf,
               label=term,
               linewidth=2)
    ax.set_title('Vehicle Density Membership Functions')
    ax.set_xlabel('Number of Vehicles')
    ax.set_ylabel('Membership Degree')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot waiting time (one example - North)
    ax = axes[0, 1]
    waiting_north = antecedents['waiting_north']
    for term in waiting_north.terms:
        ax.plot(waiting_north.universe,
               waiting_north[term].mf,
               label=term,
               linewidth=2)
    ax.set_title('Waiting Time Membership Functions')
    ax.set_xlabel('Waiting Time (seconds)')
    ax.set_ylabel('Membership Degree')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Plot green time output
    ax = axes[1, 0]
    for term in consequent.terms:
        ax.plot(consequent.universe,
               consequent[term].mf,
               label=term,
               linewidth=2)
    ax.set_title('Green Light Duration Membership Functions')
    ax.set_xlabel('Duration (seconds)')
    ax.set_ylabel('Membership Degree')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Hide the last subplot
    axes[1, 1].axis('off')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Membership functions saved to {save_path}")

    return fig


if __name__ == "__main__":
    # Test membership functions
    antecedents, green_time = create_membership_functions()
    print("✓ Membership functions created successfully!")
    print(f"  - Input variables: {len(antecedents)}")
    print(f"  - Output variable: green_time")

    # Visualize
    visualize_membership_functions(antecedents, green_time,
                                   save_path="membership_functions.png")
