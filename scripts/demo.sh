#!/bin/bash
# Demo script - Quick 2-minute comparison demo

set -e

echo "=================================================="
echo "  Fuzzy Traffic System - Quick Demo"
echo "=================================================="
echo
echo "Running 2-minute comparison demo..."
echo

# Run simple comparison
poetry run python examples/simple_comparison.py

echo
echo "=================================================="
echo "✅ Demo complete!"
echo
echo "For full simulation, run:"
echo "  ./scripts/run.sh"
echo "=================================================="
