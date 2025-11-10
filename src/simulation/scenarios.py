"""
Traffic Scenarios for Testing and Comparison

Defines various traffic patterns for evaluating controller performance.
"""

from typing import Dict
from dataclasses import dataclass


@dataclass
class TrafficScenario:
    """Defines a traffic scenario with arrival rates"""
    name: str
    description: str
    arrival_rates: Dict[str, float]  # vehicles per minute
    duration: float = 3600  # seconds

    @property
    def total_arrival_rate(self) -> float:
        """Total vehicles per minute across all directions"""
        return sum(self.arrival_rates.values())


# Predefined scenarios
class Scenarios:
    """Collection of predefined traffic scenarios"""

    @staticmethod
    def normal_traffic() -> TrafficScenario:
        """Balanced, moderate traffic on all directions"""
        return TrafficScenario(
            name="Normal Traffic",
            description="Balanced traffic with moderate flow on all directions",
            arrival_rates={
                'north': 12,
                'south': 12,
                'east': 12,
                'west': 12
            },
            duration=3600
        )

    @staticmethod
    def rush_hour_ns() -> TrafficScenario:
        """Heavy traffic on North-South (main road), light on East-West"""
        return TrafficScenario(
            name="Rush Hour (N-S)",
            description="Heavy North-South traffic (main road during rush hour)",
            arrival_rates={
                'north': 35,
                'south': 35,
                'east': 10,
                'west': 10
            },
            duration=3600
        )

    @staticmethod
    def rush_hour_ew() -> TrafficScenario:
        """Heavy traffic on East-West, light on North-South"""
        return TrafficScenario(
            name="Rush Hour (E-W)",
            description="Heavy East-West traffic",
            arrival_rates={
                'north': 10,
                'south': 10,
                'east': 35,
                'west': 35
            },
            duration=3600
        )

    @staticmethod
    def light_traffic() -> TrafficScenario:
        """Light traffic on all directions (late night)"""
        return TrafficScenario(
            name="Light Traffic",
            description="Light traffic on all directions (late night scenario)",
            arrival_rates={
                'north': 5,
                'south': 5,
                'east': 5,
                'west': 5
            },
            duration=3600
        )

    @staticmethod
    def asymmetric_heavy_north() -> TrafficScenario:
        """Heavy traffic only from North, light on others"""
        return TrafficScenario(
            name="Asymmetric (Heavy North)",
            description="Very heavy traffic from North only, testing adaptability",
            arrival_rates={
                'north': 45,
                'south': 8,
                'east': 8,
                'west': 8
            },
            duration=3600
        )

    @staticmethod
    def peak_congestion() -> TrafficScenario:
        """Very heavy traffic on all directions (congestion scenario)"""
        return TrafficScenario(
            name="Peak Congestion",
            description="Very heavy traffic on all directions, stress test",
            arrival_rates={
                'north': 40,
                'south': 40,
                'east': 40,
                'west': 40
            },
            duration=3600
        )

    @staticmethod
    def morning_commute() -> TrafficScenario:
        """Morning commute pattern: inbound heavy, outbound light"""
        return TrafficScenario(
            name="Morning Commute",
            description="Typical morning commute pattern (into city center)",
            arrival_rates={
                'north': 30,  # Inbound to city
                'south': 10,  # Outbound from city
                'east': 25,   # Inbound to city
                'west': 8     # Outbound from city
            },
            duration=7200  # 2 hours
        )

    @staticmethod
    def evening_commute() -> TrafficScenario:
        """Evening commute pattern: outbound heavy, inbound light"""
        return TrafficScenario(
            name="Evening Commute",
            description="Typical evening commute pattern (leaving city center)",
            arrival_rates={
                'north': 10,  # Outbound from city
                'south': 30,  # Inbound to suburbs
                'east': 8,    # Outbound from city
                'west': 25    # Inbound to suburbs
            },
            duration=7200  # 2 hours
        )

    @staticmethod
    def weekend_leisure() -> TrafficScenario:
        """Weekend leisure traffic - moderate and balanced"""
        return TrafficScenario(
            name="Weekend Leisure",
            description="Weekend traffic pattern with leisure trips",
            arrival_rates={
                'north': 15,
                'south': 18,
                'east': 15,
                'west': 18
            },
            duration=3600
        )

    @staticmethod
    def all_scenarios() -> Dict[str, TrafficScenario]:
        """Get all predefined scenarios as a dictionary"""
        return {
            'normal': Scenarios.normal_traffic(),
            'rush_ns': Scenarios.rush_hour_ns(),
            'rush_ew': Scenarios.rush_hour_ew(),
            'light': Scenarios.light_traffic(),
            'asymmetric_north': Scenarios.asymmetric_heavy_north(),
            'peak': Scenarios.peak_congestion(),
            'morning': Scenarios.morning_commute(),
            'evening': Scenarios.evening_commute(),
            'weekend': Scenarios.weekend_leisure()
        }

    @staticmethod
    def get_scenario(name: str) -> TrafficScenario:
        """
        Get a scenario by name.

        Args:
            name: Scenario name key

        Returns:
            TrafficScenario object

        Raises:
            KeyError: If scenario name not found
        """
        scenarios = Scenarios.all_scenarios()
        if name not in scenarios:
            available = ', '.join(scenarios.keys())
            raise KeyError(f"Scenario '{name}' not found. "
                         f"Available scenarios: {available}")
        return scenarios[name]


if __name__ == "__main__":
    print("=" * 70)
    print("TRAFFIC SCENARIOS")
    print("=" * 70)

    scenarios = Scenarios.all_scenarios()

    for key, scenario in scenarios.items():
        print(f"\n{scenario.name}")
        print("-" * 70)
        print(f"Key:         {key}")
        print(f"Description: {scenario.description}")
        print(f"Duration:    {scenario.duration}s ({scenario.duration/3600:.1f}h)")
        print(f"Arrival Rates (vehicles/minute):")
        for direction, rate in scenario.arrival_rates.items():
            print(f"  {direction:6s}: {rate:5.1f}")
        print(f"Total Rate:  {scenario.total_arrival_rate:.1f} vehicles/minute")
        print(f"             ({scenario.total_arrival_rate * 60:.0f} vehicles/hour)")

    print("\n" + "=" * 70)
    print("✓ Scenarios module ready!")
