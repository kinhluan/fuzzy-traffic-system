#!/bin/bash
# Visualize script - Generate membership function visualizations

set -e

echo "=================================================="
echo "  Fuzzy Traffic System - Generate Visualizations"
echo "=================================================="
echo
echo "Generating membership function diagrams..."
echo

# Generate membership functions visualization
poetry run python src/fuzzy_controller/membership_functions.py

echo
echo "=================================================="
echo "✅ Visualizations generated!"
echo
echo "Output saved to: docs/membership_functions.png"
echo "=================================================="
