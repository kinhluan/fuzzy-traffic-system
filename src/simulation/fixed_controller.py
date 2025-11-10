"""
Fixed-Time Traffic Light Controller

Traditional traffic light controller with predetermined timing.
Used as baseline for comparison with fuzzy controller.
"""

from typing import Dict, List
from dataclasses import dataclass
import logging


@dataclass
class FixedPhase:
    """Represents one phase in a fixed-time traffic light cycle"""
    name: str
    duration: float  # seconds
    north_state: str
    south_state: str
    east_state: str
    west_state: str


class FixedTimeController:
    """
    Traditional fixed-time traffic light controller.

    Uses predetermined timing regardless of traffic conditions.
    Common pattern: 40s green + 3s yellow + 2s all-red for each axis.
    """

    def __init__(self,
                 ns_green: float = 40.0,
                 ew_green: float = 40.0,
                 yellow_time: float = 3.0,
                 all_red_time: float = 2.0):
        """
        Initialize fixed-time controller.

        Args:
            ns_green: Green light duration for North-South axis (seconds)
            ew_green: Green light duration for East-West axis (seconds)
            yellow_time: Yellow light duration (seconds)
            all_red_time: All-red clearance time (seconds)
        """
        self.logger = logging.getLogger(__name__)

        self.ns_green = ns_green
        self.ew_green = ew_green
        self.yellow_time = yellow_time
        self.all_red_time = all_red_time

        # Build the fixed cycle
        self.phases = self._build_cycle()
        self.cycle_duration = sum(phase.duration for phase in self.phases)
        self.current_phase_index = 0
        self.time_in_current_phase = 0.0

        self.logger.info("Fixed-Time Controller initialized")
        self.logger.info(f"  N-S green: {ns_green}s")
        self.logger.info(f"  E-W green: {ew_green}s")
        self.logger.info(f"  Cycle duration: {self.cycle_duration}s")

    def _build_cycle(self) -> List[FixedPhase]:
        """Build the complete traffic light cycle"""
        phases = []

        # Phase 1: North-South Green
        phases.append(FixedPhase(
            name="NS_GREEN",
            duration=self.ns_green,
            north_state="green",
            south_state="green",
            east_state="red",
            west_state="red"
        ))

        # Phase 2: North-South Yellow
        phases.append(FixedPhase(
            name="NS_YELLOW",
            duration=self.yellow_time,
            north_state="yellow",
            south_state="yellow",
            east_state="red",
            west_state="red"
        ))

        # Phase 3: All Red (clearance)
        phases.append(FixedPhase(
            name="ALL_RED_1",
            duration=self.all_red_time,
            north_state="red",
            south_state="red",
            east_state="red",
            west_state="red"
        ))

        # Phase 4: East-West Green
        phases.append(FixedPhase(
            name="EW_GREEN",
            duration=self.ew_green,
            north_state="red",
            south_state="red",
            east_state="green",
            west_state="green"
        ))

        # Phase 5: East-West Yellow
        phases.append(FixedPhase(
            name="EW_YELLOW",
            duration=self.yellow_time,
            north_state="red",
            south_state="red",
            east_state="yellow",
            west_state="yellow"
        ))

        # Phase 6: All Red (clearance)
        phases.append(FixedPhase(
            name="ALL_RED_2",
            duration=self.all_red_time,
            north_state="red",
            south_state="red",
            east_state="red",
            west_state="red"
        ))

        return phases

    def get_current_phase(self) -> FixedPhase:
        """Get the current phase"""
        return self.phases[self.current_phase_index]

    def get_light_states(self) -> Dict[str, str]:
        """
        Get current light states for all directions.

        Returns:
            Dictionary mapping direction to light state ('red', 'yellow', 'green')
        """
        phase = self.get_current_phase()
        return {
            'north': phase.north_state,
            'south': phase.south_state,
            'east': phase.east_state,
            'west': phase.west_state
        }

    def step(self, time_step: float = 1.0):
        """
        Advance the controller by one time step.

        Args:
            time_step: Time interval (seconds)
        """
        self.time_in_current_phase += time_step

        # Check if we need to move to next phase
        current_phase = self.get_current_phase()
        if self.time_in_current_phase >= current_phase.duration:
            # Move to next phase
            self.current_phase_index = (self.current_phase_index + 1) % len(self.phases)
            self.time_in_current_phase = 0.0

            new_phase = self.get_current_phase()
            self.logger.debug(f"Phase change: {current_phase.name} -> {new_phase.name}")

    def get_time_until_next_green(self, direction: str) -> float:
        """
        Calculate time until next green light for a direction.

        Args:
            direction: Direction name ('north', 'south', 'east', 'west')

        Returns:
            Time in seconds until next green light
        """
        time_remaining = 0.0
        current_phase = self.get_current_phase()

        # Time remaining in current phase
        time_remaining = current_phase.duration - self.time_in_current_phase

        # Check subsequent phases
        phase_index = (self.current_phase_index + 1) % len(self.phases)

        while True:
            phase = self.phases[phase_index]

            # Check if this phase gives green to our direction
            light_state = getattr(phase, f"{direction}_state")
            if light_state == "green":
                return time_remaining

            time_remaining += phase.duration
            phase_index = (phase_index + 1) % len(self.phases)

            # Prevent infinite loop (shouldn't happen with valid config)
            if phase_index == self.current_phase_index:
                break

        return time_remaining

    def reset(self):
        """Reset controller to initial state"""
        self.current_phase_index = 0
        self.time_in_current_phase = 0.0
        self.logger.info("Fixed-Time Controller reset")

    def get_schedule(self) -> List[Dict]:
        """
        Get the complete traffic light schedule for one cycle.

        Returns:
            List of phase dictionaries
        """
        schedule = []
        current_time = 0.0

        for phase in self.phases:
            schedule.append({
                'phase': phase.name,
                'start_time': current_time,
                'duration': phase.duration,
                'north': phase.north_state,
                'south': phase.south_state,
                'east': phase.east_state,
                'west': phase.west_state
            })
            current_time += phase.duration

        return schedule


if __name__ == "__main__":
    # Test the fixed-time controller
    logging.basicConfig(level=logging.INFO)

    print("=" * 70)
    print("FIXED-TIME CONTROLLER TEST")
    print("=" * 70)

    controller = FixedTimeController(
        ns_green=40.0,
        ew_green=30.0,
        yellow_time=3.0,
        all_red_time=2.0
    )

    print(f"\nCycle Duration: {controller.cycle_duration}s")
    print(f"Number of Phases: {len(controller.phases)}\n")

    print("Full Cycle Schedule:")
    print("-" * 70)
    schedule = controller.get_schedule()
    for phase in schedule:
        print(f"{phase['phase']:12s} | {phase['start_time']:5.0f}s - "
              f"{phase['start_time'] + phase['duration']:5.0f}s | "
              f"N:{phase['north']:6s} S:{phase['south']:6s} "
              f"E:{phase['east']:6s} W:{phase['west']:6s}")

    print("\n" + "=" * 70)
    print("SIMULATION: 2 Complete Cycles")
    print("=" * 70)

    simulation_time = 0.0
    time_step = 1.0
    max_time = controller.cycle_duration * 2

    print(f"\n{'Time':>6s} | {'Phase':12s} | {'North':6s} | {'South':6s} | "
          f"{'East':6s} | {'West':6s}")
    print("-" * 70)

    while simulation_time < max_time:
        phase = controller.get_current_phase()
        states = controller.get_light_states()

        if simulation_time % 5 == 0:  # Print every 5 seconds
            print(f"{simulation_time:6.0f} | {phase.name:12s} | "
                  f"{states['north']:6s} | {states['south']:6s} | "
                  f"{states['east']:6s} | {states['west']:6s}")

        controller.step(time_step)
        simulation_time += time_step

    print("\n" + "=" * 70)
    print("Time Until Next Green (at t=0):")
    print("-" * 70)
    controller.reset()
    for direction in ['north', 'south', 'east', 'west']:
        time_to_green = controller.get_time_until_next_green(direction)
        print(f"{direction.capitalize():6s}: {time_to_green:6.1f}s")

    print("\n✓ Fixed-Time Controller test completed!")
