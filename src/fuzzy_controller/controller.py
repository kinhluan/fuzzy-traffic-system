"""
Fuzzy Traffic Light Controller

Main controller implementing Mamdani inference for traffic light control.
"""

import numpy as np
from skfuzzy import control as ctrl
from typing import Dict, Optional, List
import logging

from .membership_functions import create_membership_functions
from .fuzzy_rules import create_all_fuzzy_rules


class FuzzyTrafficController:
    """
    Fuzzy Logic Traffic Light Controller using Mamdani inference.

    Uses vehicle density and waiting time across all four directions
    to compute optimal green light duration for each direction.
    """

    def __init__(self, enable_logging: bool = False):
        """
        Initialize the fuzzy traffic controller.

        Args:
            enable_logging: Enable detailed logging for debugging
        """
        self.logger = logging.getLogger(__name__)
        if enable_logging:
            logging.basicConfig(level=logging.INFO)

        # Create membership functions
        self.logger.info("Creating membership functions...")
        self.antecedents, self.consequent = create_membership_functions()

        # Create fuzzy rules for all directions
        self.logger.info("Creating fuzzy rules...")
        self.all_rules = create_all_fuzzy_rules(self.antecedents, self.consequent)

        # Create control systems for each direction
        self.logger.info("Building control systems...")
        self.control_systems = {}
        self.controllers = {}

        for direction in ['north', 'south', 'east', 'west']:
            # Create control system with rules for this direction
            self.control_systems[direction] = ctrl.ControlSystem(
                self.all_rules[direction]
            )
            # Create simulation controller
            self.controllers[direction] = ctrl.ControlSystemSimulation(
                self.control_systems[direction]
            )

        self.logger.info("✓ Fuzzy Traffic Controller initialized successfully!")
        self.logger.info(f"  - Directions: 4 (N, S, E, W)")
        self.logger.info(f"  - Rules per direction: {len(self.all_rules['north'])}")
        self.logger.info(f"  - Total rules: {sum(len(r) for r in self.all_rules.values())}")

    def compute_green_time(self,
                          direction: str,
                          traffic_state: Dict[str, Dict[str, float]]) -> float:
        """
        Compute optimal green light duration for a specific direction.

        Args:
            direction: Traffic direction ('north', 'south', 'east', 'west')
            traffic_state: Dictionary containing:
                - 'density': {direction: vehicle_count} for all 4 directions
                - 'waiting_time': {direction: seconds} for all 4 directions

        Returns:
            Optimal green light duration in seconds

        Example:
            >>> traffic_state = {
            ...     'density': {'north': 75, 'south': 30, 'east': 50, 'west': 40},
            ...     'waiting_time': {'north': 120, 'south': 45, 'east': 80, 'west': 60}
            ... }
            >>> green_time = controller.compute_green_time('north', traffic_state)
        """
        if direction not in self.controllers:
            raise ValueError(f"Invalid direction: {direction}. "
                           f"Must be one of: north, south, east, west")

        controller = self.controllers[direction]

        # Set inputs for all directions
        for dir_name in ['north', 'south', 'east', 'west']:
            # Set density
            density_value = traffic_state['density'].get(dir_name, 0)
            controller.input[f'density_{dir_name}'] = np.clip(density_value, 0, 100)

            # Set waiting time
            waiting_value = traffic_state['waiting_time'].get(dir_name, 0)
            controller.input[f'waiting_{dir_name}'] = np.clip(waiting_value, 0, 300)

        # Compute output using Mamdani inference
        try:
            controller.compute()
            green_time = controller.output['green_time']

            self.logger.debug(f"{direction.upper()} - Green time: {green_time:.1f}s "
                            f"(density: {traffic_state['density'][direction]}, "
                            f"waiting: {traffic_state['waiting_time'][direction]:.1f}s)")

            return green_time

        except Exception as e:
            self.logger.error(f"Error computing green time for {direction}: {e}")
            # Return default medium green time on error
            return 40.0

    def compute_all_green_times(self,
                               traffic_state: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """
        Compute green times for all four directions.

        Args:
            traffic_state: Dictionary containing density and waiting_time for all directions

        Returns:
            Dictionary mapping each direction to its optimal green time
        """
        green_times = {}

        for direction in ['north', 'south', 'east', 'west']:
            green_times[direction] = self.compute_green_time(direction, traffic_state)

        return green_times

    def get_traffic_light_schedule(self,
                                   traffic_state: Dict[str, Dict[str, float]],
                                   yellow_time: float = 3.0,
                                   all_red_time: float = 2.0) -> List[Dict]:
        """
        Generate complete traffic light schedule for a full cycle.

        Args:
            traffic_state: Current traffic state
            yellow_time: Duration of yellow light (seconds)
            all_red_time: Duration when all lights are red (seconds)

        Returns:
            List of phase dictionaries with timing and active directions
        """
        # Compute green times for all directions
        green_times = self.compute_all_green_times(traffic_state)

        schedule = []
        current_time = 0

        # Phase 1: North-South green
        ns_green = (green_times['north'] + green_times['south']) / 2
        schedule.append({
            'phase': 'NS_GREEN',
            'start_time': current_time,
            'duration': ns_green,
            'north': 'green',
            'south': 'green',
            'east': 'red',
            'west': 'red'
        })
        current_time += ns_green

        # Yellow transition
        schedule.append({
            'phase': 'NS_YELLOW',
            'start_time': current_time,
            'duration': yellow_time,
            'north': 'yellow',
            'south': 'yellow',
            'east': 'red',
            'west': 'red'
        })
        current_time += yellow_time

        # All red
        schedule.append({
            'phase': 'ALL_RED_1',
            'start_time': current_time,
            'duration': all_red_time,
            'north': 'red',
            'south': 'red',
            'east': 'red',
            'west': 'red'
        })
        current_time += all_red_time

        # Phase 2: East-West green
        ew_green = (green_times['east'] + green_times['west']) / 2
        schedule.append({
            'phase': 'EW_GREEN',
            'start_time': current_time,
            'duration': ew_green,
            'north': 'red',
            'south': 'red',
            'east': 'green',
            'west': 'green'
        })
        current_time += ew_green

        # Yellow transition
        schedule.append({
            'phase': 'EW_YELLOW',
            'start_time': current_time,
            'duration': yellow_time,
            'north': 'red',
            'south': 'red',
            'east': 'yellow',
            'west': 'yellow'
        })
        current_time += yellow_time

        # All red
        schedule.append({
            'phase': 'ALL_RED_2',
            'start_time': current_time,
            'duration': all_red_time,
            'north': 'red',
            'south': 'red',
            'east': 'red',
            'west': 'red'
        })
        current_time += all_red_time

        return schedule

    def get_cycle_duration(self, traffic_state: Dict[str, Dict[str, float]]) -> float:
        """
        Calculate total cycle duration based on current traffic state.

        Args:
            traffic_state: Current traffic state

        Returns:
            Total cycle duration in seconds
        """
        schedule = self.get_traffic_light_schedule(traffic_state)
        return sum(phase['duration'] for phase in schedule)


if __name__ == "__main__":
    # Test the controller
    print("Initializing Fuzzy Traffic Controller...")
    controller = FuzzyTrafficController(enable_logging=True)

    # Test scenario 1: Rush hour on North-South
    print("\n" + "=" * 70)
    print("TEST SCENARIO 1: Rush Hour (Heavy North-South Traffic)")
    print("=" * 70)
    traffic_state = {
        'density': {
            'north': 85,
            'south': 80,
            'east': 25,
            'west': 20
        },
        'waiting_time': {
            'north': 150,
            'south': 140,
            'east': 30,
            'west': 25
        }
    }

    green_times = controller.compute_all_green_times(traffic_state)
    print("\nComputed Green Times:")
    for direction, time in green_times.items():
        print(f"  {direction.capitalize():6s}: {time:5.1f} seconds")

    # Test scenario 2: Balanced traffic
    print("\n" + "=" * 70)
    print("TEST SCENARIO 2: Balanced Traffic")
    print("=" * 70)
    traffic_state = {
        'density': {
            'north': 50,
            'south': 50,
            'east': 50,
            'west': 50
        },
        'waiting_time': {
            'north': 60,
            'south': 60,
            'east': 60,
            'west': 60
        }
    }

    green_times = controller.compute_all_green_times(traffic_state)
    print("\nComputed Green Times:")
    for direction, time in green_times.items():
        print(f"  {direction.capitalize():6s}: {time:5.1f} seconds")

    # Test scenario 3: Light traffic
    print("\n" + "=" * 70)
    print("TEST SCENARIO 3: Light Traffic")
    print("=" * 70)
    traffic_state = {
        'density': {
            'north': 10,
            'south': 15,
            'east': 12,
            'west': 8
        },
        'waiting_time': {
            'north': 20,
            'south': 25,
            'east': 18,
            'west': 15
        }
    }

    green_times = controller.compute_all_green_times(traffic_state)
    print("\nComputed Green Times:")
    for direction, time in green_times.items():
        print(f"  {direction.capitalize():6s}: {time:5.1f} seconds")

    print("\n✓ Fuzzy Traffic Controller test completed!")
