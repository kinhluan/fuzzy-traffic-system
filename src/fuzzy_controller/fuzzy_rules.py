"""
Advanced Fuzzy Rules for Traffic Light Control

Implements 28 fuzzy rules covering:
1. Primary density-based rules (12 rules)
2. Waiting time priority rules (8 rules)
3. Fairness and balance rules (8 rules)
"""

from skfuzzy import control as ctrl
from typing import Dict, List


def create_fuzzy_rules(antecedents: Dict[str, ctrl.Antecedent],
                      consequent: ctrl.Consequent,
                      direction: str = 'north') -> List[ctrl.Rule]:
    """
    Create fuzzy rules for a specific traffic direction.

    Args:
        antecedents: Dictionary of input variables
        consequent: Output variable (green_time)
        direction: Traffic direction ('north', 'south', 'east', 'west')

    Returns:
        List of fuzzy rules for the specified direction
    """

    # Get direction-specific variables
    current_density = antecedents[f'density_{direction}']
    current_waiting = antecedents[f'waiting_{direction}']

    # Get opposite direction (for N-S or E-W axis)
    opposite_map = {
        'north': 'south',
        'south': 'north',
        'east': 'west',
        'west': 'east'
    }
    opposite_dir = opposite_map[direction]
    opposite_density = antecedents[f'density_{opposite_dir}']
    opposite_waiting = antecedents[f'waiting_{opposite_dir}']

    # Get perpendicular directions
    if direction in ['north', 'south']:
        perp_dir1, perp_dir2 = 'east', 'west'
    else:
        perp_dir1, perp_dir2 = 'north', 'south'

    perp_density1 = antecedents[f'density_{perp_dir1}']
    perp_density2 = antecedents[f'density_{perp_dir2}']
    perp_waiting1 = antecedents[f'waiting_{perp_dir1}']
    perp_waiting2 = antecedents[f'waiting_{perp_dir2}']

    rules = []

    # ========================================================================
    # CATEGORY 1: PRIMARY DENSITY-BASED RULES (12 rules)
    # ========================================================================

    # Rule 1: High current density + Low opposite density = Very Long green
    rules.append(ctrl.Rule(
        current_density['high'] & opposite_density['low'],
        consequent['very_long'],
        label=f'R1_{direction}_high_opp_low'
    ))

    # Rule 2: High current density + Medium opposite density = Long green
    rules.append(ctrl.Rule(
        current_density['high'] & opposite_density['medium'],
        consequent['long'],
        label=f'R2_{direction}_high_opp_med'
    ))

    # Rule 3: High current density + High opposite density = Medium green (balance)
    rules.append(ctrl.Rule(
        current_density['high'] & opposite_density['high'],
        consequent['medium'],
        label=f'R3_{direction}_high_opp_high'
    ))

    # Rule 4: Medium current density + Low opposite density = Long green
    rules.append(ctrl.Rule(
        current_density['medium'] & opposite_density['low'],
        consequent['long'],
        label=f'R4_{direction}_med_opp_low'
    ))

    # Rule 5: Medium current density + Medium opposite density = Medium green
    rules.append(ctrl.Rule(
        current_density['medium'] & opposite_density['medium'],
        consequent['medium'],
        label=f'R5_{direction}_med_opp_med'
    ))

    # Rule 6: Medium current density + High opposite density = Short green
    rules.append(ctrl.Rule(
        current_density['medium'] & opposite_density['high'],
        consequent['short'],
        label=f'R6_{direction}_med_opp_high'
    ))

    # Rule 7: Low current density + Low opposite density = Short green
    rules.append(ctrl.Rule(
        current_density['low'] & opposite_density['low'],
        consequent['short'],
        label=f'R7_{direction}_low_opp_low'
    ))

    # Rule 8: Low current density + Medium opposite density = Short green
    rules.append(ctrl.Rule(
        current_density['low'] & opposite_density['medium'],
        consequent['short'],
        label=f'R8_{direction}_low_opp_med'
    ))

    # Rule 9: Low current density + High opposite density = Short green
    rules.append(ctrl.Rule(
        current_density['low'] & opposite_density['high'],
        consequent['short'],
        label=f'R9_{direction}_low_opp_high'
    ))

    # Rule 10: High density regardless of opposite = at least Medium
    rules.append(ctrl.Rule(
        current_density['high'],
        consequent['medium'],
        label=f'R10_{direction}_high_minimum'
    ))

    # Rule 11: Medium current + Low opposite, but perpendicular is high = Medium (fairness)
    rules.append(ctrl.Rule(
        current_density['medium'] & opposite_density['low'] &
        (perp_density1['high'] | perp_density2['high']),
        consequent['medium'],
        label=f'R11_{direction}_fairness_perp'
    ))

    # Rule 12: Low density but very long waiting = Medium (prevent starvation)
    rules.append(ctrl.Rule(
        current_density['low'] & current_waiting['very_long'],
        consequent['medium'],
        label=f'R12_{direction}_starvation_prevent'
    ))

    # ========================================================================
    # CATEGORY 2: WAITING TIME PRIORITY RULES (8 rules)
    # ========================================================================

    # Rule 13: Very long waiting time = prioritize with Long green
    rules.append(ctrl.Rule(
        current_waiting['very_long'],
        consequent['long'],
        label=f'R13_{direction}_very_long_wait'
    ))

    # Rule 14: Long waiting + High density = Very Long green (emergency priority)
    rules.append(ctrl.Rule(
        current_waiting['long'] & current_density['high'],
        consequent['very_long'],
        label=f'R14_{direction}_long_wait_high_dens'
    ))

    # Rule 15: Long waiting + Medium density = Long green
    rules.append(ctrl.Rule(
        current_waiting['long'] & current_density['medium'],
        consequent['long'],
        label=f'R15_{direction}_long_wait_med_dens'
    ))

    # Rule 16: Medium waiting + Low density = Medium green
    rules.append(ctrl.Rule(
        current_waiting['medium'] & current_density['low'],
        consequent['medium'],
        label=f'R16_{direction}_med_wait_low_dens'
    ))

    # Rule 17: Short waiting + High density = Long green (density priority)
    rules.append(ctrl.Rule(
        current_waiting['short'] & current_density['high'],
        consequent['long'],
        label=f'R17_{direction}_short_wait_high_dens'
    ))

    # Rule 18: Current very long wait, but opposite also very long = Medium (fairness)
    rules.append(ctrl.Rule(
        current_waiting['very_long'] & opposite_waiting['very_long'],
        consequent['medium'],
        label=f'R18_{direction}_both_very_long_wait'
    ))

    # Rule 19: Long wait + perpendicular very long wait = Medium (global fairness)
    rules.append(ctrl.Rule(
        current_waiting['long'] &
        (perp_waiting1['very_long'] | perp_waiting2['very_long']),
        consequent['medium'],
        label=f'R19_{direction}_perp_very_long_wait'
    ))

    # Rule 20: Medium wait + all other directions short wait = Long green
    rules.append(ctrl.Rule(
        current_waiting['medium'] &
        opposite_waiting['short'] &
        perp_waiting1['short'] &
        perp_waiting2['short'],
        consequent['long'],
        label=f'R20_{direction}_only_waiting'
    ))

    # ========================================================================
    # CATEGORY 3: FAIRNESS AND BALANCE RULES (8 rules)
    # ========================================================================

    # Rule 21: High density everywhere = Medium green (rotate fairly)
    rules.append(ctrl.Rule(
        current_density['high'] &
        opposite_density['high'] &
        perp_density1['high'] &
        perp_density2['high'],
        consequent['medium'],
        label=f'R21_{direction}_all_high_dens'
    ))

    # Rule 22: Current high, all others low = Very Long (maximize throughput)
    rules.append(ctrl.Rule(
        current_density['high'] &
        opposite_density['low'] &
        perp_density1['low'] &
        perp_density2['low'],
        consequent['very_long'],
        label=f'R22_{direction}_only_high_dens'
    ))

    # Rule 23: Current medium, all others high = Short (give way)
    rules.append(ctrl.Rule(
        current_density['medium'] &
        opposite_density['high'] &
        perp_density1['high'] &
        perp_density2['high'],
        consequent['short'],
        label=f'R23_{direction}_give_way'
    ))

    # Rule 24: Balanced density everywhere = Medium green
    rules.append(ctrl.Rule(
        current_density['medium'] &
        opposite_density['medium'] &
        perp_density1['medium'] &
        perp_density2['medium'],
        consequent['medium'],
        label=f'R24_{direction}_balanced'
    ))

    # Rule 25: High current + High perpendicular = Medium (prevent cross-blocking)
    rules.append(ctrl.Rule(
        current_density['high'] &
        (perp_density1['high'] | perp_density2['high']),
        consequent['medium'],
        label=f'R25_{direction}_prevent_blocking'
    ))

    # Rule 26: Low current, high perpendicular waiting = Short (switch quickly)
    rules.append(ctrl.Rule(
        current_density['low'] &
        (perp_waiting1['long'] | perp_waiting2['long']),
        consequent['short'],
        label=f'R26_{direction}_quick_switch'
    ))

    # Rule 27: Medium density + opposite low + perpendicular medium = Long
    rules.append(ctrl.Rule(
        current_density['medium'] &
        opposite_density['low'] &
        perp_density1['medium'] &
        perp_density2['medium'],
        consequent['long'],
        label=f'R27_{direction}_opportunistic'
    ))

    # Rule 28: High wait + low density + opposite high density = Medium (balance)
    rules.append(ctrl.Rule(
        current_waiting['long'] &
        current_density['low'] &
        opposite_density['high'],
        consequent['medium'],
        label=f'R28_{direction}_wait_vs_density_balance'
    ))

    return rules


def create_all_fuzzy_rules(antecedents: Dict[str, ctrl.Antecedent],
                           consequent: ctrl.Consequent) -> Dict[str, List[ctrl.Rule]]:
    """
    Create fuzzy rules for all four directions.

    Args:
        antecedents: Dictionary of input variables
        consequent: Output variable (green_time)

    Returns:
        Dictionary mapping direction to its list of rules
    """
    all_rules = {}

    for direction in ['north', 'south', 'east', 'west']:
        all_rules[direction] = create_fuzzy_rules(antecedents, consequent, direction)

    return all_rules


def print_rules_summary(all_rules: Dict[str, List[ctrl.Rule]]):
    """Print a summary of all created rules."""
    print("=" * 70)
    print("FUZZY RULES SUMMARY")
    print("=" * 70)

    for direction, rules in all_rules.items():
        print(f"\n{direction.upper()} Direction: {len(rules)} rules")
        print("-" * 70)

        # Group by category
        primary = [r for r in rules if r.label.startswith(f'R{1}') or
                   int(r.label.split('_')[0][1:]) <= 12]
        waiting = [r for r in rules if 13 <= int(r.label.split('_')[0][1:]) <= 20]
        fairness = [r for r in rules if int(r.label.split('_')[0][1:]) >= 21]

        print(f"  Primary Density Rules:    {len(primary)}")
        print(f"  Waiting Time Rules:       {len(waiting)}")
        print(f"  Fairness & Balance Rules: {len(fairness)}")

    print("\n" + "=" * 70)
    total_rules = sum(len(rules) for rules in all_rules.values())
    print(f"TOTAL RULES ACROSS ALL DIRECTIONS: {total_rules}")
    print("=" * 70)


if __name__ == "__main__":
    from membership_functions import create_membership_functions

    # Create membership functions
    antecedents, green_time = create_membership_functions()

    # Create rules for all directions
    all_rules = create_all_fuzzy_rules(antecedents, green_time)

    # Print summary
    print_rules_summary(all_rules)

    # Example: Print first 5 rules for North
    print("\n\nExample: First 5 rules for NORTH direction:")
    print("-" * 70)
    for i, rule in enumerate(all_rules['north'][:5], 1):
        print(f"{i}. {rule.label}")
