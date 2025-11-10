"""
Queue-Based Traffic Simulation Model

Implements a simple but realistic traffic simulation using queuing theory.
Vehicles arrive according to Poisson distribution and depart during green lights.
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging


class LightState(Enum):
    """Traffic light states"""
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


@dataclass
class Vehicle:
    """Represents a single vehicle in the system"""
    id: int
    arrival_time: float
    direction: str
    departed: bool = False
    departure_time: Optional[float] = None

    @property
    def waiting_time(self) -> float:
        """Calculate current waiting time"""
        if self.departed and self.departure_time:
            return self.departure_time - self.arrival_time
        return 0.0


@dataclass
class DirectionState:
    """State of traffic in one direction"""
    name: str
    queue: List[Vehicle] = field(default_factory=list)
    light_state: LightState = LightState.RED
    total_arrivals: int = 0
    total_departures: int = 0
    total_waiting_time: float = 0.0
    arrival_rate: float = 10.0  # vehicles per minute

    @property
    def queue_length(self) -> int:
        """Current queue length"""
        return len(self.queue)

    @property
    def average_waiting_time(self) -> float:
        """Average waiting time of departed vehicles"""
        if self.total_departures == 0:
            return 0.0
        return self.total_waiting_time / self.total_departures

    @property
    def current_waiting_time(self) -> float:
        """Waiting time of first vehicle in queue"""
        if len(self.queue) == 0:
            return 0.0
        return self.queue[0].waiting_time if self.queue[0].departed else 0.0


class TrafficSimulator:
    """
    Queue-based traffic simulator for a 4-way intersection.

    Uses Poisson arrival process and realistic departure during green lights.
    """

    def __init__(self,
                 arrival_rates: Optional[Dict[str, float]] = None,
                 departure_rate: float = 0.5,  # seconds per vehicle
                 simulation_duration: float = 3600,  # 1 hour default
                 random_seed: Optional[int] = None):
        """
        Initialize traffic simulator.

        Args:
            arrival_rates: Vehicle arrival rates (vehicles/minute) for each direction
                         Default: {'north': 10, 'south': 10, 'east': 10, 'west': 10}
            departure_rate: Time for one vehicle to pass through (seconds)
            simulation_duration: Total simulation time (seconds)
            random_seed: Random seed for reproducibility
        """
        self.logger = logging.getLogger(__name__)

        # Set random seed
        if random_seed is not None:
            np.random.seed(random_seed)

        # Initialize directions
        self.directions = {}
        default_rates = {'north': 10, 'south': 10, 'east': 10, 'west': 10}
        rates = arrival_rates or default_rates

        for direction in ['north', 'south', 'east', 'west']:
            self.directions[direction] = DirectionState(
                name=direction,
                arrival_rate=rates.get(direction, 10.0)
            )

        self.departure_rate = departure_rate
        self.simulation_duration = simulation_duration
        self.current_time = 0.0
        self.vehicle_id_counter = 0

        # Statistics
        self.total_vehicles_generated = 0
        self.total_vehicles_departed = 0
        self.event_log = []

        self.logger.info("Traffic Simulator initialized")
        self.logger.info(f"  Simulation duration: {simulation_duration}s")
        self.logger.info(f"  Arrival rates: {rates}")

    def generate_arrivals(self, time_step: float = 1.0):
        """
        Generate vehicle arrivals for the next time step using Poisson distribution.

        Args:
            time_step: Time interval for arrivals (seconds)
        """
        for direction, state in self.directions.items():
            # Convert arrival rate from vehicles/minute to vehicles/second
            lambda_rate = state.arrival_rate / 60.0

            # Number of arrivals in this time step (Poisson distribution)
            num_arrivals = np.random.poisson(lambda_rate * time_step)

            for _ in range(num_arrivals):
                vehicle = Vehicle(
                    id=self.vehicle_id_counter,
                    arrival_time=self.current_time,
                    direction=direction
                )
                state.queue.append(vehicle)
                state.total_arrivals += 1
                self.vehicle_id_counter += 1
                self.total_vehicles_generated += 1

                self.logger.debug(f"t={self.current_time:.1f}: Vehicle {vehicle.id} "
                                f"arrived at {direction}")

    def process_departures(self, time_step: float = 1.0):
        """
        Process vehicle departures for directions with green lights.

        Args:
            time_step: Time interval for processing departures (seconds)
        """
        for direction, state in self.directions.items():
            if state.light_state != LightState.GREEN:
                continue

            # Calculate how many vehicles can depart in this time step
            max_departures = int(time_step / self.departure_rate)

            departures_count = 0
            while state.queue and departures_count < max_departures:
                vehicle = state.queue.pop(0)
                vehicle.departed = True
                vehicle.departure_time = self.current_time

                waiting_time = vehicle.waiting_time
                state.total_waiting_time += waiting_time
                state.total_departures += 1
                self.total_vehicles_departed += 1
                departures_count += 1

                self.logger.debug(f"t={self.current_time:.1f}: Vehicle {vehicle.id} "
                                f"departed from {direction} "
                                f"(waited {waiting_time:.1f}s)")

    def set_light_state(self, direction: str, state: LightState):
        """
        Set traffic light state for a direction.

        Args:
            direction: Direction name
            state: New light state
        """
        old_state = self.directions[direction].light_state
        self.directions[direction].light_state = state

        if old_state != state:
            self.event_log.append({
                'time': self.current_time,
                'event': 'light_change',
                'direction': direction,
                'from': old_state.value,
                'to': state.value
            })
            self.logger.debug(f"t={self.current_time:.1f}: {direction} light: "
                            f"{old_state.value} -> {state.value}")

    def set_all_lights(self, states: Dict[str, LightState]):
        """
        Set light states for all directions.

        Args:
            states: Dictionary mapping direction to light state
        """
        for direction, state in states.items():
            self.set_light_state(direction, state)

    def step(self, time_step: float = 1.0):
        """
        Advance simulation by one time step.

        Args:
            time_step: Duration of time step (seconds)
        """
        self.generate_arrivals(time_step)
        self.process_departures(time_step)
        self.current_time += time_step

    def get_traffic_state(self) -> Dict[str, Dict[str, float]]:
        """
        Get current traffic state for fuzzy controller input.

        Returns:
            Dictionary with 'density' and 'waiting_time' for each direction
        """
        traffic_state = {
            'density': {},
            'waiting_time': {}
        }

        for direction, state in self.directions.items():
            # Density is queue length (normalized to 0-100 scale)
            # Assume max queue of 50 vehicles = 100% density
            traffic_state['density'][direction] = min(state.queue_length * 2, 100)

            # Waiting time of first vehicle in queue
            if state.queue:
                # Use the waiting time since arrival
                waiting = self.current_time - state.queue[0].arrival_time
                traffic_state['waiting_time'][direction] = min(waiting, 300)
            else:
                traffic_state['waiting_time'][direction] = 0.0

        return traffic_state

    def get_statistics(self) -> Dict:
        """
        Get simulation statistics.

        Returns:
            Dictionary containing performance metrics
        """
        stats = {
            'simulation_time': self.current_time,
            'total_arrivals': self.total_vehicles_generated,
            'total_departures': self.total_vehicles_departed,
            'vehicles_in_system': self.total_vehicles_generated - self.total_vehicles_departed,
            'directions': {}
        }

        for direction, state in self.directions.items():
            stats['directions'][direction] = {
                'arrivals': state.total_arrivals,
                'departures': state.total_departures,
                'current_queue_length': state.queue_length,
                'average_waiting_time': state.average_waiting_time,
                'total_waiting_time': state.total_waiting_time
            }

        # Overall metrics
        total_waiting = sum(s['total_waiting_time']
                          for s in stats['directions'].values())
        total_departures = sum(s['departures']
                             for s in stats['directions'].values())

        stats['average_waiting_time'] = (
            total_waiting / total_departures if total_departures > 0 else 0
        )
        stats['total_queue_length'] = sum(s['current_queue_length']
                                         for s in stats['directions'].values())

        return stats

    def reset(self):
        """Reset simulation to initial state"""
        for direction in self.directions.values():
            direction.queue.clear()
            direction.light_state = LightState.RED
            direction.total_arrivals = 0
            direction.total_departures = 0
            direction.total_waiting_time = 0.0

        self.current_time = 0.0
        self.vehicle_id_counter = 0
        self.total_vehicles_generated = 0
        self.total_vehicles_departed = 0
        self.event_log.clear()

        self.logger.info("Simulation reset")


if __name__ == "__main__":
    # Test the simulator
    logging.basicConfig(level=logging.INFO)

    print("=" * 70)
    print("TRAFFIC SIMULATOR TEST")
    print("=" * 70)

    # Create simulator with different arrival rates
    arrival_rates = {
        'north': 20,  # Heavy traffic
        'south': 20,  # Heavy traffic
        'east': 10,   # Medium traffic
        'west': 10    # Medium traffic
    }

    sim = TrafficSimulator(
        arrival_rates=arrival_rates,
        simulation_duration=300,  # 5 minutes
        random_seed=42
    )

    # Simulate simple fixed-time control
    print("\nSimulating 60 seconds with simple fixed-time control...")
    print("Phase 1: North-South GREEN for 20s")

    for t in range(60):
        if t < 20:
            # North-South green
            sim.set_all_lights({
                'north': LightState.GREEN,
                'south': LightState.GREEN,
                'east': LightState.RED,
                'west': LightState.RED
            })
        elif t < 23:
            # Yellow transition
            sim.set_all_lights({
                'north': LightState.YELLOW,
                'south': LightState.YELLOW,
                'east': LightState.RED,
                'west': LightState.RED
            })
        elif t < 25:
            # All red
            sim.set_all_lights({
                'north': LightState.RED,
                'south': LightState.RED,
                'east': LightState.RED,
                'west': LightState.RED
            })
        elif t < 45:
            # East-West green
            sim.set_all_lights({
                'north': LightState.RED,
                'south': LightState.RED,
                'east': LightState.GREEN,
                'west': LightState.GREEN
            })
        elif t < 48:
            # Yellow transition
            sim.set_all_lights({
                'north': LightState.RED,
                'south': LightState.RED,
                'east': LightState.YELLOW,
                'west': LightState.YELLOW
            })
        else:
            # All red
            sim.set_all_lights({
                'north': LightState.RED,
                'south': LightState.RED,
                'east': LightState.RED,
                'west': LightState.RED
            })

        sim.step(time_step=1.0)

        if t % 10 == 0:
            state = sim.get_traffic_state()
            print(f"\nTime {t}s:")
            for direction in ['north', 'south', 'east', 'west']:
                print(f"  {direction:5s}: density={state['density'][direction]:5.1f}, "
                      f"waiting={state['waiting_time'][direction]:6.1f}s, "
                      f"queue={sim.directions[direction].queue_length:3d}")

    # Print final statistics
    print("\n" + "=" * 70)
    print("SIMULATION STATISTICS")
    print("=" * 70)
    stats = sim.get_statistics()

    print(f"\nOverall:")
    print(f"  Simulation time:       {stats['simulation_time']:.1f}s")
    print(f"  Total arrivals:        {stats['total_arrivals']}")
    print(f"  Total departures:      {stats['total_departures']}")
    print(f"  Vehicles in system:    {stats['vehicles_in_system']}")
    print(f"  Average waiting time:  {stats['average_waiting_time']:.2f}s")
    print(f"  Total queue length:    {stats['total_queue_length']}")

    print(f"\nBy Direction:")
    for direction, dir_stats in stats['directions'].items():
        print(f"  {direction.upper()}:")
        print(f"    Arrivals:      {dir_stats['arrivals']}")
        print(f"    Departures:    {dir_stats['departures']}")
        print(f"    Queue length:  {dir_stats['current_queue_length']}")
        print(f"    Avg wait time: {dir_stats['average_waiting_time']:.2f}s")

    print("\n✓ Traffic Simulator test completed!")
