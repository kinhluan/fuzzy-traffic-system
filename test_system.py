"""
System Test Script

Quick test to verify all components are working.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

print("=" * 70)
print("FUZZY TRAFFIC SYSTEM - COMPONENT TESTS")
print("=" * 70)

# Test 1: Membership Functions
print("\n[1/5] Testing Membership Functions...")
try:
    from fuzzy_controller.membership_functions import create_membership_functions
    antecedents, consequent = create_membership_functions()
    print(f"✓ Created {len(antecedents)} input variables and 1 output variable")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Test 2: Fuzzy Rules
print("\n[2/5] Testing Fuzzy Rules...")
try:
    from fuzzy_controller.fuzzy_rules import create_all_fuzzy_rules
    all_rules = create_all_fuzzy_rules(antecedents, consequent)
    total_rules = sum(len(rules) for rules in all_rules.values())
    print(f"✓ Created {total_rules} fuzzy rules across 4 directions")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Test 3: Fuzzy Controller
print("\n[3/5] Testing Fuzzy Controller...")
try:
    from fuzzy_controller.controller import FuzzyTrafficController
    controller = FuzzyTrafficController(enable_logging=False)

    # Test computation
    traffic_state = {
        'density': {'north': 75, 'south': 30, 'east': 50, 'west': 40},
        'waiting_time': {'north': 120, 'south': 45, 'east': 80, 'west': 60}
    }
    green_time = controller.compute_green_time('north', traffic_state)
    print(f"✓ Fuzzy controller working (sample output: {green_time:.1f}s)")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Test 4: Traffic Simulator
print("\n[4/5] Testing Traffic Simulator...")
try:
    from simulation.traffic_model import TrafficSimulator, LightState

    sim = TrafficSimulator(
        arrival_rates={'north': 10, 'south': 10, 'east': 10, 'west': 10},
        simulation_duration=60,
        random_seed=42
    )

    # Run for 10 steps
    for _ in range(10):
        sim.set_light_state('north', LightState.GREEN)
        sim.step(1.0)

    stats = sim.get_statistics()
    print(f"✓ Traffic simulator working ({stats['total_arrivals']} arrivals)")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Test 5: Fixed-Time Controller
print("\n[5/5] Testing Fixed-Time Controller...")
try:
    from simulation.fixed_controller import FixedTimeController

    fixed = FixedTimeController(ns_green=40, ew_green=40)
    states = fixed.get_light_states()
    print(f"✓ Fixed-time controller working (cycle: {fixed.cycle_duration}s)")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Test 6: Scenarios
print("\n[6/6] Testing Traffic Scenarios...")
try:
    from simulation.scenarios import Scenarios

    scenarios = Scenarios.all_scenarios()
    print(f"✓ Loaded {len(scenarios)} traffic scenarios")
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Summary
print("\n" + "=" * 70)
print("ALL TESTS PASSED! ✓")
print("=" * 70)
print("\nYou can now:")
print("  1. Run full comparison: poetry run python src/main.py")
print("  2. Run simple demo: poetry run python examples/simple_comparison.py")
print("  3. Open web/index.html in browser to view dashboard")
print("\nTo deploy to GitHub Pages:")
print("  1. Push code to GitHub")
print("  2. Enable Pages in repo settings (Settings → Pages → Source: /web)")
print("=" * 70)
