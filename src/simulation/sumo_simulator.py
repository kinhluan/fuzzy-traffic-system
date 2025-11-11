"""
SUMO Traffic Simulator Integration
Connects fuzzy traffic controller to SUMO via TraCI API
"""

import os
import sys
from typing import Dict, List, Tuple
from dataclasses import dataclass

try:
    import traci
    TRACI_AVAILABLE = True
except ImportError:
    TRACI_AVAILABLE = False
    print("Warning: TraCI not available. Install with: pip install traci")


@dataclass
class SUMOMetrics:
    """Metrics collected from SUMO simulation"""
    avg_waiting_time: float
    max_waiting_time: float
    avg_queue_length: float
    max_queue_length: float
    throughput: float
    total_vehicles: int
    total_waiting_time: float
    fairness_index: float


class SUMOSimulator:
    """
    SUMO simulator wrapper for fuzzy traffic light control

    Integrates with SUMO via TraCI to:
    - Collect real-time traffic data (density, waiting times)
    - Apply fuzzy controller decisions (green light duration)
    - Measure performance metrics
    """

    def __init__(
        self,
        sumo_cfg: str,
        tls_id: str = "center",
        use_gui: bool = True,
        step_length: float = 1.0
    ):
        """
        Initialize SUMO simulator

        Args:
            sumo_cfg: Path to SUMO configuration file (.sumocfg)
            tls_id: Traffic light system ID (junction name)
            use_gui: Whether to use SUMO-GUI (visual) or sumo (headless)
            step_length: Simulation step length in seconds
        """
        if not TRACI_AVAILABLE:
            raise ImportError("TraCI not installed. Run: pip install traci")

        self.sumo_cfg = sumo_cfg
        self.tls_id = tls_id
        self.use_gui = use_gui
        self.step_length = step_length

        # Direction mapping: SUMO edge -> controller direction
        self.direction_map = {
            'north': 'north_in',
            'south': 'south_in',
            'east': 'east_in',
            'west': 'west_in'
        }

        # Traffic light phases (SUMO uses phases for signal states)
        # Phase 0: North-South green
        # Phase 2: East-West green
        self.phases = {
            'north_south': 0,
            'east_west': 2
        }

        # Metrics tracking
        self.total_waiting_time = 0.0
        self.vehicle_count = 0
        self.waiting_times: Dict[str, List[float]] = {
            'north': [], 'south': [], 'east': [], 'west': []
        }
        self.queue_lengths: Dict[str, List[int]] = {
            'north': [], 'south': [], 'east': [], 'west': []
        }

    def start(self):
        """Start SUMO simulation"""
        sumo_binary = "sumo-gui" if self.use_gui else "sumo"
        sumo_cmd = [sumo_binary, "-c", self.sumo_cfg, "--step-length", str(self.step_length)]

        try:
            traci.start(sumo_cmd)
            print(f"SUMO started: {sumo_binary}")
            print(f"Configuration: {self.sumo_cfg}")
            print(f"Traffic light ID: {self.tls_id}")
        except Exception as e:
            raise RuntimeError(f"Failed to start SUMO: {e}")

    def step(self, num_steps: int = 1):
        """Execute simulation steps"""
        for _ in range(num_steps):
            traci.simulationStep()

    def close(self):
        """Close SUMO simulation"""
        try:
            traci.close()
            print("SUMO closed")
        except Exception as e:
            print(f"Error closing SUMO: {e}")

    def get_traffic_state(self) -> Dict[str, Dict[str, float]]:
        """
        Get current traffic state for all directions

        Returns:
            Dictionary with density and waiting time for each direction
            {
                'north': {'density': 15, 'waiting_time': 25.5},
                'south': {'density': 10, 'waiting_time': 18.0},
                ...
            }
        """
        state = {}

        for direction, edge_id in self.direction_map.items():
            # Get vehicles on this edge
            vehicle_ids = traci.edge.getLastStepVehicleIDs(edge_id)

            # Calculate density (number of vehicles)
            density = len(vehicle_ids)

            # Calculate average waiting time for vehicles on this edge
            if vehicle_ids:
                waiting_times = [
                    traci.vehicle.getWaitingTime(veh_id)
                    for veh_id in vehicle_ids
                ]
                avg_waiting_time = sum(waiting_times) / len(waiting_times)
            else:
                avg_waiting_time = 0.0

            state[direction] = {
                'density': density,
                'waiting_time': avg_waiting_time
            }

            # Track metrics
            self.waiting_times[direction].append(avg_waiting_time)
            self.queue_lengths[direction].append(density)

        return state

    def set_green_time(self, direction: str, duration: int):
        """
        Set green light duration for specified direction

        Args:
            direction: 'north', 'south', 'east', or 'west'
            duration: Green time in seconds
        """
        # Determine phase based on direction
        if direction in ['north', 'south']:
            phase_index = self.phases['north_south']
        else:  # east or west
            phase_index = self.phases['east_west']

        # Set traffic light phase
        traci.trafficlight.setPhase(self.tls_id, phase_index)

        # Hold green for specified duration
        traci.trafficlight.setPhaseDuration(self.tls_id, duration)

    def get_current_phase(self) -> str:
        """Get current traffic light phase"""
        phase_index = traci.trafficlight.getPhase(self.tls_id)

        if phase_index == self.phases['north_south']:
            return 'north_south'
        elif phase_index == self.phases['east_west']:
            return 'east_west'
        else:
            return 'unknown'

    def get_simulation_time(self) -> float:
        """Get current simulation time in seconds"""
        return traci.simulation.getTime()

    def get_vehicle_count(self) -> int:
        """Get total number of vehicles in simulation"""
        return traci.vehicle.getIDCount()

    def get_departed_vehicles(self) -> int:
        """Get number of vehicles that have departed"""
        return traci.simulation.getDepartedNumber()

    def get_arrived_vehicles(self) -> int:
        """Get number of vehicles that have arrived (completed journey)"""
        return traci.simulation.getArrivedNumber()

    def calculate_metrics(self) -> SUMOMetrics:
        """
        Calculate performance metrics from collected data

        Returns:
            SUMOMetrics object with comprehensive performance data
        """
        # Aggregate waiting times across all directions
        all_waiting_times = []
        for direction_times in self.waiting_times.values():
            all_waiting_times.extend(direction_times)

        # Aggregate queue lengths
        all_queue_lengths = []
        for direction_queues in self.queue_lengths.values():
            all_queue_lengths.extend(direction_queues)

        # Calculate averages
        avg_waiting = sum(all_waiting_times) / len(all_waiting_times) if all_waiting_times else 0.0
        max_waiting = max(all_waiting_times) if all_waiting_times else 0.0
        avg_queue = sum(all_queue_lengths) / len(all_queue_lengths) if all_queue_lengths else 0.0
        max_queue = max(all_queue_lengths) if all_queue_lengths else 0.0

        # Throughput: vehicles that completed journey
        total_vehicles = self.get_departed_vehicles()
        arrived_vehicles = self.get_arrived_vehicles()
        simulation_time = self.get_simulation_time()

        # Throughput in vehicles per hour
        throughput = (arrived_vehicles / simulation_time * 3600) if simulation_time > 0 else 0.0

        # Calculate fairness index (Jain's Fairness Index)
        direction_avg_waiting = [
            sum(times) / len(times) if times else 0.0
            for times in self.waiting_times.values()
        ]

        if direction_avg_waiting and sum(direction_avg_waiting) > 0:
            numerator = sum(direction_avg_waiting) ** 2
            denominator = len(direction_avg_waiting) * sum(t ** 2 for t in direction_avg_waiting)
            fairness = numerator / denominator if denominator > 0 else 1.0
        else:
            fairness = 1.0

        return SUMOMetrics(
            avg_waiting_time=avg_waiting,
            max_waiting_time=max_waiting,
            avg_queue_length=avg_queue,
            max_queue_length=max_queue,
            throughput=throughput,
            total_vehicles=total_vehicles,
            total_waiting_time=sum(all_waiting_times),
            fairness_index=fairness
        )

    def reset_metrics(self):
        """Reset metric tracking"""
        self.total_waiting_time = 0.0
        self.vehicle_count = 0
        self.waiting_times = {k: [] for k in self.waiting_times}
        self.queue_lengths = {k: [] for k in self.queue_lengths}


def check_sumo_installation() -> bool:
    """
    Check if SUMO is properly installed

    Returns:
        True if SUMO is available, False otherwise
    """
    if not TRACI_AVAILABLE:
        print("TraCI Python module not found")
        print("Install with: pip install traci")
        return False

    # Check if SUMO_HOME environment variable is set
    if 'SUMO_HOME' not in os.environ:
        print("SUMO_HOME environment variable not set")
        print("Please set SUMO_HOME to your SUMO installation directory")
        return False

    sumo_home = os.environ['SUMO_HOME']
    print(f"SUMO_HOME: {sumo_home}")

    # Check if sumo and sumo-gui binaries exist
    sumo_binary = os.path.join(sumo_home, 'bin', 'sumo')
    sumo_gui_binary = os.path.join(sumo_home, 'bin', 'sumo-gui')

    if sys.platform == 'win32':
        sumo_binary += '.exe'
        sumo_gui_binary += '.exe'

    if not os.path.exists(sumo_binary):
        print(f"SUMO binary not found: {sumo_binary}")
        return False

    print(f"SUMO installation found: {sumo_binary}")
    return True


if __name__ == "__main__":
    # Test SUMO installation
    print("Checking SUMO installation...")
    if check_sumo_installation():
        print("✓ SUMO is properly installed")
    else:
        print("✗ SUMO installation issues detected")
