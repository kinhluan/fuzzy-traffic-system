"""Quick test for simulation fixes"""
import sys
sys.path.insert(0, 'src')

from fuzzy_controller.controller import FuzzyTrafficController
from simulation.traffic_model import TrafficSimulator, LightState
from simulation.scenarios import Scenarios
from utils.metrics import PerformanceMetrics

# Test with light traffic scenario (faster)
scenario = Scenarios.get_scenario('light')
print(f"Testing: {scenario.name}")
print(f"Arrival rates: {scenario.arrival_rates}")

simulator = TrafficSimulator(
    arrival_rates=scenario.arrival_rates,
    simulation_duration=60,  # Just 60 seconds for quick test
    random_seed=42
)
controller = FuzzyTrafficController(enable_logging=False)
metrics = PerformanceMetrics(simulation_duration=60)

# Initialize
current_phase = 'init'
phase_start_time = 0.0
phase_duration = 0.0
time_step = 1.0

for _ in range(60):  # 60 steps
    traffic_state = simulator.get_traffic_state()
    
    # Simple phase control
    time_in_phase = simulator.current_time - phase_start_time
    
    if time_in_phase >= phase_duration:
        if current_phase == 'init' or current_phase == 'ew_green':
            # NS green
            ns_green = 20
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
            # EW green
            ew_green = 20
            phase_duration = ew_green
            phase_start_time = simulator.current_time
            current_phase = 'ew_green'
            simulator.set_all_lights({
                'north': LightState.RED,
                'south': LightState.RED,
                'east': LightState.GREEN,
                'west': LightState.GREEN
            })
    
    # Step
    simulator.step(time_step)
    
    # Record departures
    for direction, dir_state in simulator.directions.items():
        for vehicle in dir_state.recent_departures:
            metrics.record_departure(direction, vehicle.waiting_time)

# Check results
stats = simulator.get_statistics()
print(f"\nSimulation Results (60s):")
print(f"  Total arrivals: {stats['total_arrivals']}")
print(f"  Total departures: {stats['total_departures']}")
print(f"  Vehicles in system: {stats['vehicles_in_system']}")

summary = metrics.get_summary()
print(f"\nMetrics:")
print(f"  Avg waiting time: {summary['average_waiting_time']:.2f}s")
print(f"  Throughput: {summary['throughput_per_hour']:.1f} veh/h")

if stats['total_departures'] > 0 and summary['average_waiting_time'] > 0:
    print("\n✅ SIMULATION WORKING!")
else:
    print("\n⚠️  WARNING: No departures or zero waiting time")
