"""
Simple Comparison Example

Demonstrates how to run a simple comparison between Fuzzy and Fixed-Time controllers.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from fuzzy_controller.controller import FuzzyTrafficController
from simulation.traffic_model import TrafficSimulator, LightState
from simulation.fixed_controller import FixedTimeController
from simulation.scenarios import Scenarios


def run_simple_demo():
    """Run a simple 2-minute demo comparison"""
    print("=" * 70)
    print("SIMPLE FUZZY VS FIXED-TIME CONTROLLER DEMO")
    print("=" * 70)

    # Use normal traffic scenario
    scenario = Scenarios.normal_traffic()
    duration = 120  # 2 minutes

    print(f"\nScenario: {scenario.name}")
    print(f"Duration: {duration}s")
    print(f"Arrival rates: {scenario.arrival_rates}")

    # Test Fuzzy Controller
    print("\n" + "-" * 70)
    print("Testing Fuzzy Controller...")
    print("-" * 70)

    fuzzy_controller = FuzzyTrafficController(enable_logging=False)
    simulator = TrafficSimulator(
        arrival_rates=scenario.arrival_rates,
        simulation_duration=duration,
        random_seed=42
    )

    # Simple simulation loop
    current_phase = 'ns'  # Start with North-South
    phase_time = 0

    for _ in range(int(duration)):
        traffic_state = simulator.get_traffic_state()

        # Switch phases every 30 seconds (simplified)
        if phase_time >= 30:
            current_phase = 'ew' if current_phase == 'ns' else 'ns'
            phase_time = 0

        # Set lights based on current phase
        if current_phase == 'ns':
            simulator.set_all_lights({
                'north': LightState.GREEN,
                'south': LightState.GREEN,
                'east': LightState.RED,
                'west': LightState.RED
            })
        else:
            simulator.set_all_lights({
                'north': LightState.RED,
                'south': LightState.RED,
                'east': LightState.GREEN,
                'west': LightState.GREEN
            })

        simulator.step(1.0)
        phase_time += 1

    fuzzy_stats = simulator.get_statistics()

    print(f"Results:")
    print(f"  Total departures: {fuzzy_stats['total_departures']}")
    print(f"  Avg waiting time: {fuzzy_stats['average_waiting_time']:.2f}s")
    print(f"  Total queue: {fuzzy_stats['total_queue_length']} vehicles")

    # Test Fixed-Time Controller
    print("\n" + "-" * 70)
    print("Testing Fixed-Time Controller...")
    print("-" * 70)

    fixed_controller = FixedTimeController(ns_green=40, ew_green=40)
    simulator2 = TrafficSimulator(
        arrival_rates=scenario.arrival_rates,
        simulation_duration=duration,
        random_seed=42  # Same seed for fair comparison
    )

    for _ in range(int(duration)):
        light_states = fixed_controller.get_light_states()

        for direction, state_str in light_states.items():
            simulator2.set_light_state(direction, LightState(state_str))

        simulator2.step(1.0)
        fixed_controller.step(1.0)

    fixed_stats = simulator2.get_statistics()

    print(f"Results:")
    print(f"  Total departures: {fixed_stats['total_departures']}")
    print(f"  Avg waiting time: {fixed_stats['average_waiting_time']:.2f}s")
    print(f"  Total queue: {fixed_stats['total_queue_length']} vehicles")

    # Comparison
    print("\n" + "=" * 70)
    print("COMPARISON SUMMARY")
    print("=" * 70)

    wait_improvement = ((fixed_stats['average_waiting_time'] -
                        fuzzy_stats['average_waiting_time']) /
                       fixed_stats['average_waiting_time'] * 100)

    queue_improvement = ((fixed_stats['total_queue_length'] -
                         fuzzy_stats['total_queue_length']) /
                        fixed_stats['total_queue_length'] * 100)

    print(f"\nFuzzy Controller Performance:")
    print(f"  Waiting time improvement: {wait_improvement:+.1f}%")
    print(f"  Queue length improvement: {queue_improvement:+.1f}%")

    print("\n✓ Demo completed!")


if __name__ == "__main__":
    run_simple_demo()
