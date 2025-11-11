"""
SUMO + Fuzzy Controller Demo
Demonstrates fuzzy traffic light control with SUMO simulation
"""

import os
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from fuzzy_controller.membership_functions import create_membership_functions
from fuzzy_controller.fuzzy_rules import create_fuzzy_rules
from fuzzy_controller.controller import FuzzyTrafficController
from simulation.sumo_simulator import SUMOSimulator, check_sumo_installation


def run_fuzzy_sumo_demo(
    sumo_cfg: str,
    simulation_duration: int = 600,
    use_gui: bool = True
):
    """
    Run fuzzy traffic controller with SUMO

    Args:
        sumo_cfg: Path to SUMO configuration file
        simulation_duration: Total simulation time in seconds
        use_gui: Whether to show SUMO GUI
    """
    print("=" * 60)
    print("FUZZY TRAFFIC CONTROLLER + SUMO DEMO")
    print("=" * 60)

    # Check SUMO installation
    print("\n[1/5] Checking SUMO installation...")
    if not check_sumo_installation():
        print("ERROR: SUMO not properly installed")
        print("\nPlease install SUMO and set SUMO_HOME environment variable")
        return

    # Initialize fuzzy controller
    print("\n[2/5] Initializing fuzzy traffic controller...")
    try:
        membership_funcs, green_time = create_membership_functions()
        fuzzy_rules = create_fuzzy_rules(membership_funcs, green_time)
        controller = FuzzyTrafficController(membership_funcs, green_time, fuzzy_rules)
        print("✓ Fuzzy controller ready (28 rules per direction)")
    except Exception as e:
        print(f"ERROR initializing controller: {e}")
        return

    # Initialize SUMO simulator
    print("\n[3/5] Initializing SUMO simulator...")
    try:
        simulator = SUMOSimulator(
            sumo_cfg=sumo_cfg,
            tls_id="center",
            use_gui=use_gui,
            step_length=1.0
        )
        simulator.start()
        print("✓ SUMO started successfully")
    except Exception as e:
        print(f"ERROR starting SUMO: {e}")
        return

    # Run simulation
    print(f"\n[4/5] Running simulation ({simulation_duration} seconds)...")
    print("\nTime(s) | Phase    | N-Density | S-Density | E-Density | W-Density | Green(s)")
    print("-" * 80)

    try:
        current_time = 0
        current_phase = 'north_south'
        phase_start_time = 0

        while current_time < simulation_duration:
            # Get current traffic state
            traffic_state = simulator.get_traffic_state()

            # Determine which direction to control based on current phase
            if current_phase == 'north_south':
                active_direction = 'north'
            else:  # east_west
                active_direction = 'east'

            # Get green time from fuzzy controller
            densities = {d: traffic_state[d]['density'] for d in traffic_state}
            waiting_times = {d: traffic_state[d]['waiting_time'] for d in traffic_state}

            green_duration = controller.compute_green_time(
                direction=active_direction,
                densities=densities,
                waiting_times=waiting_times
            )

            # Apply decision to SUMO
            simulator.set_green_time(active_direction, int(green_duration))

            # Print status every 10 seconds
            if current_time % 10 == 0:
                print(
                    f"{current_time:6d}  | {current_phase:8s} | "
                    f"{densities['north']:9.0f} | {densities['south']:9.0f} | "
                    f"{densities['east']:9.0f} | {densities['west']:9.0f} | "
                    f"{green_duration:7.1f}"
                )

            # Execute simulation steps
            simulator.step(int(green_duration))

            # Update time and switch phase
            current_time += green_duration
            phase_start_time = current_time

            # Switch phase
            current_phase = 'east_west' if current_phase == 'north_south' else 'north_south'

    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user")

    except Exception as e:
        print(f"\n\nERROR during simulation: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Calculate and display results
        print("\n[5/5] Calculating metrics...")
        try:
            metrics = simulator.calculate_metrics()

            print("\n" + "=" * 60)
            print("SIMULATION RESULTS")
            print("=" * 60)
            print(f"Simulation Time:      {simulator.get_simulation_time():.1f} seconds")
            print(f"Total Vehicles:       {metrics.total_vehicles}")
            print(f"Completed Journeys:   {simulator.get_arrived_vehicles()}")
            print()
            print(f"Avg Waiting Time:     {metrics.avg_waiting_time:.2f} seconds")
            print(f"Max Waiting Time:     {metrics.max_waiting_time:.2f} seconds")
            print(f"Avg Queue Length:     {metrics.avg_queue_length:.2f} vehicles")
            print(f"Max Queue Length:     {metrics.max_queue_length:.0f} vehicles")
            print(f"Throughput:           {metrics.throughput:.2f} vehicles/hour")
            print(f"Fairness Index:       {metrics.fairness_index:.4f}")
            print("=" * 60)

        except Exception as e:
            print(f"ERROR calculating metrics: {e}")

        # Close SUMO
        simulator.close()
        print("\nDemo completed!")


def main():
    """Main entry point"""
    # Determine paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    sumo_cfg = project_root / "sumo_files" / "configs" / "single_intersection.sumocfg"

    # Check if config file exists
    if not sumo_cfg.exists():
        print(f"ERROR: SUMO configuration file not found: {sumo_cfg}")
        print("\nPlease ensure SUMO network files are generated first.")
        print("Run: cd sumo_files/networks && netconvert --node-files=single_intersection.nod.xml --edge-files=single_intersection.edg.xml --type-files=single_intersection.typ.xml --output-file=single_intersection.net.xml")
        return

    # Run demo
    print(f"Using SUMO config: {sumo_cfg}")
    print("\nOptions:")
    print("  - Press Ctrl+C to stop simulation early")
    print("  - Close SUMO window to end simulation")
    print()

    run_fuzzy_sumo_demo(
        sumo_cfg=str(sumo_cfg),
        simulation_duration=600,  # 10 minutes
        use_gui=True  # Set to False for headless mode
    )


if __name__ == "__main__":
    main()
