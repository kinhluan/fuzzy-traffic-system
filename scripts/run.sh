#!/bin/bash
# Run script - Execute full comparison simulation

set -e

echo "=================================================="
echo "  Fuzzy Traffic System - Full Simulation"
echo "=================================================="
echo
echo "Running comparison across all scenarios..."
echo "This may take 5-10 minutes..."
echo

# Run main simulation
poetry run python src/main.py

echo
echo "=================================================="
echo "✅ Simulation complete!"
echo
echo "Results saved to: web/data/comparison_results.json"
echo
echo "To view results:"
echo "  1. Open web/index.html in browser"
echo "  2. Or run: ./scripts/serve.sh"
echo "=================================================="
