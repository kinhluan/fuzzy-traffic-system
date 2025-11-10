"""
Main Comparison Script

Compares Fuzzy Controller vs Fixed-Time Controller across different scenarios.
Generates comprehensive analysis and exports results for web visualization.
"""

import json
import logging
from typing import Dict, Tuple
from pathlib import Path

from fuzzy_controller.controller import FuzzyTrafficController
from simulation.traffic_model import TrafficSimulator, LightState
from simulation.fixed_controller import FixedTimeController
from simulation.scenarios import Scenarios
from utils.metrics import PerformanceMetrics


def run_simulation_with_fuzzy(scenario, duration: float = 1800) -> PerformanceMetrics:
    """
    Run simulation with fuzzy controller.

    Args:
        scenario: TrafficScenario object
        duration: Simulation duration in seconds

    Returns:
        PerformanceMetrics object
    """
    print(f"  Running with Fuzzy Controller...")

    # Initialize
    simulator = TrafficSimulator(
        arrival_rates=scenario.arrival_rates,
        simulation_duration=duration,
        random_seed=42
    )
    controller = FuzzyTrafficController(enable_logging=False)
    metrics = PerformanceMetrics(simulation_duration=duration)

    time_step = 1.0
    current_phase = 'init'  # Start with initialization phase
    phase_start_time = 0.0
    phase_duration = 0.0

    while simulator.current_time < duration:
        # Get current traffic state
        traffic_state = simulator.get_traffic_state()

        # Record metrics
        queue_state = {
            'queue_lengths': {d: simulator.directions[d].queue_length
                            for d in ['north', 'south', 'east', 'west']}
        }
        metrics.record_timestep(simulator.current_time, queue_state)

        # Check if we need to compute new phase duration
        time_in_phase = simulator.current_time - phase_start_time

        if time_in_phase >= phase_duration:
            # Switch phase based on current state
            if current_phase == 'init':
                # Initialize with NS green
                ns_green = (controller.compute_green_time('north', traffic_state) +
                           controller.compute_green_time('south', traffic_state)) / 2
                phase_duration = ns_green
                phase_start_time = simulator.current_time
                current_phase = 'ns_green'
                simulator.set_all_lights({
                    'north': LightState.GREEN,
                    'south': LightState.GREEN,
                    'east': LightState.RED,
                    'west': LightState.RED
                })
            elif current_phase == 'ns_green':
                # NS green finished, go to yellow
                phase_duration = 3.0
                phase_start_time = simulator.current_time
                current_phase = 'ns_yellow'
                simulator.set_all_lights({
                    'north': LightState.YELLOW,
                    'south': LightState.YELLOW,
                    'east': LightState.RED,
                    'west': LightState.RED
                })
            elif current_phase == 'ns_yellow':
                # NS yellow finished, go to all red
                phase_duration = 2.0
                phase_start_time = simulator.current_time
                current_phase = 'all_red_1'
                simulator.set_all_lights({d: LightState.RED
                                        for d in ['north', 'south', 'east', 'west']})
            elif current_phase == 'all_red_1':
                # Compute green time for EW
                ew_green = (controller.compute_green_time('east', traffic_state) +
                           controller.compute_green_time('west', traffic_state)) / 2
                phase_duration = ew_green
                phase_start_time = simulator.current_time
                current_phase = 'ew_green'
                simulator.set_all_lights({
                    'north': LightState.RED,
                    'south': LightState.RED,
                    'east': LightState.GREEN,
                    'west': LightState.GREEN
                })
            elif current_phase == 'ew_green':
                phase_duration = 3.0
                phase_start_time = simulator.current_time
                current_phase = 'ew_yellow'
                simulator.set_all_lights({
                    'north': LightState.RED,
                    'south': LightState.RED,
                    'east': LightState.YELLOW,
                    'west': LightState.YELLOW
                })
            elif current_phase == 'ew_yellow':
                phase_duration = 2.0
                phase_start_time = simulator.current_time
                current_phase = 'all_red_2'
                simulator.set_all_lights({d: LightState.RED
                                        for d in ['north', 'south', 'east', 'west']})
            elif current_phase == 'all_red_2':
                # Back to NS green
                ns_green = (controller.compute_green_time('north', traffic_state) +
                           controller.compute_green_time('south', traffic_state)) / 2
                phase_duration = ns_green
                phase_start_time = simulator.current_time
                current_phase = 'ns_green'
                simulator.set_all_lights({
                    'north': LightState.GREEN,
                    'south': LightState.GREEN,
                    'east': LightState.RED,
                    'west': LightState.RED
                })

        # Step simulation
        simulator.step(time_step)

        # Record departures from this timestep
        for direction, dir_state in simulator.directions.items():
            for vehicle in dir_state.recent_departures:
                metrics.record_departure(direction, vehicle.waiting_time)

    return metrics


def run_simulation_with_fixed(scenario, duration: float = 1800) -> PerformanceMetrics:
    """
    Run simulation with fixed-time controller.

    Args:
        scenario: TrafficScenario object
        duration: Simulation duration in seconds

    Returns:
        PerformanceMetrics object
    """
    print(f"  Running with Fixed-Time Controller...")

    # Initialize
    simulator = TrafficSimulator(
        arrival_rates=scenario.arrival_rates,
        simulation_duration=duration,
        random_seed=42  # Same seed for fair comparison
    )
    controller = FixedTimeController(ns_green=40, ew_green=40,
                                     yellow_time=3, all_red_time=2)
    metrics = PerformanceMetrics(simulation_duration=duration)

    time_step = 1.0

    while simulator.current_time < duration:
        # Get light states from fixed controller
        light_states = controller.get_light_states()

        # Apply to simulator
        for direction, state_str in light_states.items():
            simulator.set_light_state(direction, LightState(state_str))

        # Record metrics
        queue_state = {
            'queue_lengths': {d: simulator.directions[d].queue_length
                            for d in ['north', 'south', 'east', 'west']}
        }
        metrics.record_timestep(simulator.current_time, queue_state)

        # Step both simulator and controller
        simulator.step(time_step)
        controller.step(time_step)

        # Record departures from this timestep
        for direction, dir_state in simulator.directions.items():
            for vehicle in dir_state.recent_departures:
                metrics.record_departure(direction, vehicle.waiting_time)

    return metrics


def compare_scenarios():
    """Run comparison across all scenarios and generate results"""
    print("=" * 70)
    print("FUZZY VS FIXED-TIME TRAFFIC CONTROLLER COMPARISON")
    print("=" * 70)

    scenarios = Scenarios.all_scenarios()
    results = {}

    for scenario_key, scenario in scenarios.items():
        print(f"\n{'='*70}")
        print(f"Scenario: {scenario.name}")
        print(f"{'='*70}")
        print(f"Description: {scenario.description}")
        print(f"Duration: {scenario.duration}s")
        print(f"Arrival rates: {scenario.arrival_rates}")

        # Run with fuzzy
        fuzzy_metrics = run_simulation_with_fuzzy(scenario, duration=min(scenario.duration, 1800))

        # Run with fixed
        fixed_metrics = run_simulation_with_fixed(scenario, duration=min(scenario.duration, 1800))

        # Print comparison
        print(f"\n{'-'*70}")
        print("FUZZY CONTROLLER RESULTS:")
        print(f"{'-'*70}")
        fuzzy_summary = fuzzy_metrics.get_summary()
        print(f"  Avg Waiting Time:     {fuzzy_summary['average_waiting_time']:.2f}s")
        print(f"  Max Waiting Time:     {fuzzy_summary['max_waiting_time']:.2f}s")
        print(f"  Avg Queue Length:     {fuzzy_summary['average_queue_length']:.2f}")
        print(f"  Max Queue Length:     {fuzzy_summary['max_queue_length']}")
        print(f"  Throughput:           {fuzzy_summary['throughput_per_hour']:.1f} veh/h")
        print(f"  Fairness Index:       {fuzzy_summary['fairness_index']:.3f}")

        print(f"\n{'-'*70}")
        print("FIXED-TIME CONTROLLER RESULTS:")
        print(f"{'-'*70}")
        fixed_summary = fixed_metrics.get_summary()
        print(f"  Avg Waiting Time:     {fixed_summary['average_waiting_time']:.2f}s")
        print(f"  Max Waiting Time:     {fixed_summary['max_waiting_time']:.2f}s")
        print(f"  Avg Queue Length:     {fixed_summary['average_queue_length']:.2f}")
        print(f"  Max Queue Length:     {fixed_summary['max_queue_length']}")
        print(f"  Throughput:           {fixed_summary['throughput_per_hour']:.1f} veh/h")
        print(f"  Fairness Index:       {fixed_summary['fairness_index']:.3f}")

        # Calculate improvements
        comparison = fuzzy_metrics.compare_with(fixed_metrics)

        print(f"\n{'-'*70}")
        print("IMPROVEMENT (Fuzzy vs Fixed):")
        print(f"{'-'*70}")
        print(f"  Waiting Time:    {comparison['waiting_time_improvement_%']:+.1f}%")
        print(f"  Queue Length:    {comparison['queue_length_improvement_%']:+.1f}%")
        print(f"  Throughput:      {comparison['throughput_improvement_%']:+.1f}%")
        print(f"  Delay Reduction: {comparison['delay_reduction_%']:+.1f}%")
        print(f"  Fairness:        {comparison['fairness_improvement']:+.3f}")

        # Store results
        results[scenario_key] = {
            'scenario': {
                'name': scenario.name,
                'description': scenario.description,
                'arrival_rates': scenario.arrival_rates
            },
            'fuzzy': fuzzy_summary,
            'fixed': fixed_summary,
            'comparison': comparison
        }

    # Export results as JSON for web visualization
    output_dir = Path('web/data')
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / 'comparison_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*70}")
    print(f"✓ Results exported to web/data/comparison_results.json")
    print(f"{'='*70}")

    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    results = compare_scenarios()
