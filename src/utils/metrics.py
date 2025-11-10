"""
Performance Metrics Calculator

Calculates and tracks performance metrics for traffic control systems.
"""

import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import pandas as pd


@dataclass
class DirectionMetrics:
    """Performance metrics for one direction"""
    direction: str
    total_arrivals: int = 0
    total_departures: int = 0
    waiting_times: List[float] = field(default_factory=list)
    queue_lengths: List[int] = field(default_factory=list)
    green_times: List[float] = field(default_factory=list)

    @property
    def average_waiting_time(self) -> float:
        """Average waiting time for departed vehicles"""
        return np.mean(self.waiting_times) if self.waiting_times else 0.0

    @property
    def max_waiting_time(self) -> float:
        """Maximum waiting time"""
        return max(self.waiting_times) if self.waiting_times else 0.0

    @property
    def average_queue_length(self) -> float:
        """Average queue length over time"""
        return np.mean(self.queue_lengths) if self.queue_lengths else 0.0

    @property
    def max_queue_length(self) -> int:
        """Maximum queue length observed"""
        return max(self.queue_lengths) if self.queue_lengths else 0

    @property
    def total_delay(self) -> float:
        """Total delay time (sum of all waiting times)"""
        return sum(self.waiting_times)

    @property
    def throughput(self) -> int:
        """Total vehicles processed"""
        return self.total_departures


@dataclass
class PerformanceMetrics:
    """
    Comprehensive performance metrics for traffic control evaluation.

    Tracks metrics including:
    - Average waiting time
    - Maximum waiting time
    - Queue lengths
    - Throughput (vehicles/hour)
    - Total delay
    - Fairness index
    """

    def __init__(self, simulation_duration: float = 3600):
        """
        Initialize performance metrics tracker.

        Args:
            simulation_duration: Total simulation duration in seconds
        """
        self.simulation_duration = simulation_duration
        self.directions: Dict[str, DirectionMetrics] = {
            'north': DirectionMetrics('north'),
            'south': DirectionMetrics('south'),
            'east': DirectionMetrics('east'),
            'west': DirectionMetrics('west')
        }

        # Time series data
        self.timestamps: List[float] = []
        self.total_queue_history: List[int] = []

    def record_timestep(self, timestamp: float, traffic_state: Dict):
        """
        Record metrics for a single timestep.

        Args:
            timestamp: Current simulation time
            traffic_state: Current traffic state from simulator
        """
        self.timestamps.append(timestamp)

        total_queue = 0
        for direction in ['north', 'south', 'east', 'west']:
            dir_metrics = self.directions[direction]

            # Record queue length
            if 'queue_lengths' in traffic_state:
                queue_len = traffic_state['queue_lengths'].get(direction, 0)
                dir_metrics.queue_lengths.append(queue_len)
                total_queue += queue_len

        self.total_queue_history.append(total_queue)

    def record_departure(self, direction: str, waiting_time: float):
        """
        Record a vehicle departure.

        Args:
            direction: Direction the vehicle departed from
            waiting_time: Total waiting time of the vehicle
        """
        self.directions[direction].waiting_times.append(waiting_time)
        self.directions[direction].total_departures += 1

    def record_arrival(self, direction: str):
        """
        Record a vehicle arrival.

        Args:
            direction: Direction where vehicle arrived
        """
        self.directions[direction].total_arrivals += 1

    def record_green_time(self, direction: str, duration: float):
        """
        Record green light duration.

        Args:
            direction: Direction that received green light
            duration: Duration in seconds
        """
        self.directions[direction].green_times.append(duration)

    # ========================================================================
    # AGGREGATE METRICS
    # ========================================================================

    @property
    def total_arrivals(self) -> int:
        """Total vehicles arrived across all directions"""
        return sum(d.total_arrivals for d in self.directions.values())

    @property
    def total_departures(self) -> int:
        """Total vehicles departed across all directions"""
        return sum(d.total_departures for d in self.directions.values())

    @property
    def total_vehicles_in_system(self) -> int:
        """Vehicles currently in the system"""
        return self.total_arrivals - self.total_departures

    @property
    def average_waiting_time(self) -> float:
        """Overall average waiting time across all directions"""
        all_waiting_times = []
        for dir_metrics in self.directions.values():
            all_waiting_times.extend(dir_metrics.waiting_times)
        return np.mean(all_waiting_times) if all_waiting_times else 0.0

    @property
    def max_waiting_time(self) -> float:
        """Maximum waiting time across all directions"""
        max_times = [d.max_waiting_time for d in self.directions.values()]
        return max(max_times) if max_times else 0.0

    @property
    def total_delay(self) -> float:
        """Total delay across all vehicles (seconds)"""
        return sum(d.total_delay for d in self.directions.values())

    @property
    def average_queue_length(self) -> float:
        """Average total queue length across all directions"""
        return np.mean(self.total_queue_history) if self.total_queue_history else 0.0

    @property
    def max_queue_length(self) -> int:
        """Maximum total queue length observed"""
        return max(self.total_queue_history) if self.total_queue_history else 0

    @property
    def throughput_per_hour(self) -> float:
        """Vehicles processed per hour"""
        if self.simulation_duration == 0:
            return 0.0
        hours = self.simulation_duration / 3600
        return self.total_departures / hours if hours > 0 else 0.0

    @property
    def fairness_index(self) -> float:
        """
        Jain's Fairness Index for waiting times across directions.

        Value ranges from 0 to 1, where 1 is perfectly fair.
        """
        avg_waiting_times = [d.average_waiting_time for d in self.directions.values()
                            if d.total_departures > 0]

        if not avg_waiting_times or len(avg_waiting_times) < 2:
            return 1.0

        n = len(avg_waiting_times)
        sum_x = sum(avg_waiting_times)
        sum_x_squared = sum(x**2 for x in avg_waiting_times)

        if sum_x_squared == 0:
            return 1.0

        fairness = (sum_x ** 2) / (n * sum_x_squared)
        return fairness

    @property
    def utilization_rate(self) -> float:
        """
        System utilization rate (percentage of time with vehicles in system).
        """
        if not self.total_queue_history:
            return 0.0

        non_zero_steps = sum(1 for q in self.total_queue_history if q > 0)
        return non_zero_steps / len(self.total_queue_history) if self.total_queue_history else 0.0

    def get_summary(self) -> Dict:
        """
        Get comprehensive summary of all metrics.

        Returns:
            Dictionary containing all performance metrics
        """
        summary = {
            'simulation_duration': self.simulation_duration,
            'total_arrivals': self.total_arrivals,
            'total_departures': self.total_departures,
            'vehicles_in_system': self.total_vehicles_in_system,

            # Time-based metrics
            'average_waiting_time': self.average_waiting_time,
            'max_waiting_time': self.max_waiting_time,
            'total_delay': self.total_delay,

            # Queue metrics
            'average_queue_length': self.average_queue_length,
            'max_queue_length': self.max_queue_length,

            # Performance metrics
            'throughput_per_hour': self.throughput_per_hour,
            'fairness_index': self.fairness_index,
            'utilization_rate': self.utilization_rate,

            # Per-direction metrics
            'by_direction': {}
        }

        for direction, metrics in self.directions.items():
            summary['by_direction'][direction] = {
                'arrivals': metrics.total_arrivals,
                'departures': metrics.total_departures,
                'avg_waiting_time': metrics.average_waiting_time,
                'max_waiting_time': metrics.max_waiting_time,
                'avg_queue_length': metrics.average_queue_length,
                'max_queue_length': metrics.max_queue_length,
                'total_delay': metrics.total_delay,
                'throughput': metrics.throughput
            }

        return summary

    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert metrics to pandas DataFrame for analysis.

        Returns:
            DataFrame with per-direction metrics
        """
        data = []
        for direction, metrics in self.directions.items():
            data.append({
                'direction': direction,
                'arrivals': metrics.total_arrivals,
                'departures': metrics.total_departures,
                'avg_waiting_time': metrics.average_waiting_time,
                'max_waiting_time': metrics.max_waiting_time,
                'avg_queue_length': metrics.average_queue_length,
                'max_queue_length': metrics.max_queue_length,
                'total_delay': metrics.total_delay,
                'throughput': metrics.throughput
            })

        return pd.DataFrame(data)

    def compare_with(self, other: 'PerformanceMetrics') -> Dict:
        """
        Compare metrics with another controller's performance.

        Args:
            other: Another PerformanceMetrics instance

        Returns:
            Dictionary showing improvements (positive = better)
        """
        comparison = {
            'waiting_time_improvement_%': (
                (other.average_waiting_time - self.average_waiting_time) /
                other.average_waiting_time * 100
                if other.average_waiting_time > 0 else 0
            ),
            'queue_length_improvement_%': (
                (other.average_queue_length - self.average_queue_length) /
                other.average_queue_length * 100
                if other.average_queue_length > 0 else 0
            ),
            'throughput_improvement_%': (
                (self.throughput_per_hour - other.throughput_per_hour) /
                other.throughput_per_hour * 100
                if other.throughput_per_hour > 0 else 0
            ),
            'delay_reduction_%': (
                (other.total_delay - self.total_delay) /
                other.total_delay * 100
                if other.total_delay > 0 else 0
            ),
            'fairness_improvement': self.fairness_index - other.fairness_index
        }

        return comparison

    def print_summary(self, title: str = "Performance Metrics"):
        """Print a formatted summary of metrics"""
        print("=" * 70)
        print(f"{title}")
        print("=" * 70)

        summary = self.get_summary()

        print(f"\nOverall Metrics:")
        print(f"  Simulation Duration:    {summary['simulation_duration']:.0f}s "
              f"({summary['simulation_duration']/3600:.1f}h)")
        print(f"  Total Arrivals:         {summary['total_arrivals']}")
        print(f"  Total Departures:       {summary['total_departures']}")
        print(f"  Vehicles in System:     {summary['vehicles_in_system']}")
        print(f"  Throughput:             {summary['throughput_per_hour']:.1f} vehicles/hour")

        print(f"\nWaiting Time Metrics:")
        print(f"  Average Waiting Time:   {summary['average_waiting_time']:.2f}s")
        print(f"  Maximum Waiting Time:   {summary['max_waiting_time']:.2f}s")
        print(f"  Total Delay:            {summary['total_delay']:.0f}s "
              f"({summary['total_delay']/3600:.1f}h)")

        print(f"\nQueue Metrics:")
        print(f"  Average Queue Length:   {summary['average_queue_length']:.2f} vehicles")
        print(f"  Maximum Queue Length:   {summary['max_queue_length']} vehicles")

        print(f"\nPerformance Indices:")
        print(f"  Fairness Index:         {summary['fairness_index']:.3f} (1.0 = perfect)")
        print(f"  Utilization Rate:       {summary['utilization_rate']:.1%}")

        print(f"\nPer-Direction Metrics:")
        for direction, metrics in summary['by_direction'].items():
            print(f"\n  {direction.upper()}:")
            print(f"    Arrivals:           {metrics['arrivals']}")
            print(f"    Departures:         {metrics['departures']}")
            print(f"    Avg Waiting Time:   {metrics['avg_waiting_time']:.2f}s")
            print(f"    Max Waiting Time:   {metrics['max_waiting_time']:.2f}s")
            print(f"    Avg Queue Length:   {metrics['avg_queue_length']:.2f}")
            print(f"    Max Queue Length:   {metrics['max_queue_length']}")


if __name__ == "__main__":
    # Test the metrics module
    print("Testing Performance Metrics Module\n")

    metrics = PerformanceMetrics(simulation_duration=3600)

    # Simulate some data
    import random
    random.seed(42)

    for direction in ['north', 'south', 'east', 'west']:
        # Simulate arrivals
        for _ in range(100):
            metrics.record_arrival(direction)

        # Simulate departures with waiting times
        for _ in range(90):
            waiting_time = random.uniform(10, 120)
            metrics.record_departure(direction, waiting_time)

    # Simulate queue length history
    for t in range(0, 3600, 10):
        queue_state = {
            'queue_lengths': {
                'north': random.randint(0, 20),
                'south': random.randint(0, 20),
                'east': random.randint(0, 15),
                'west': random.randint(0, 15)
            }
        }
        metrics.record_timestep(t, queue_state)

    # Print summary
    metrics.print_summary("Test Simulation Results")

    print("\n" + "=" * 70)
    print("✓ Performance Metrics module ready!")
