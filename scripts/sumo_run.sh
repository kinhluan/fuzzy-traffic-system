#!/bin/bash
# Run SUMO Demo with Fuzzy Traffic Controller
# Main script to run the complete demo

set -e  # Exit on error

echo "========================================="
echo "  SUMO + Fuzzy Controller Demo"
echo "========================================="
echo ""

# Determine script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
NETWORK_FILE="$PROJECT_ROOT/sumo_files/networks/single_intersection.net.xml"

# Check if network exists
if [ ! -f "$NETWORK_FILE" ]; then
    echo "❌ ERROR: Network file not found!"
    echo "   Expected: $NETWORK_FILE"
    echo ""
    echo "Please run setup first:"
    echo "  ./scripts/sumo_setup.sh"
    exit 1
fi

echo "✓ Network file found"
echo ""

# Check Python environment
if command -v poetry &> /dev/null; then
    echo "📦 Using Poetry environment"
    PYTHON_CMD="poetry run python"
elif command -v python3 &> /dev/null; then
    echo "🐍 Using python3"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    echo "🐍 Using python"
    PYTHON_CMD="python"
else
    echo "❌ ERROR: Python not found"
    exit 1
fi

# Check if TraCI is installed
$PYTHON_CMD -c "import traci" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ ERROR: TraCI not installed"
    echo ""
    echo "Install with:"
    echo "  pip install traci"
    echo "  # or"
    echo "  poetry add traci"
    exit 1
fi

echo "✓ TraCI available"
echo ""

# Run demo
echo "🚀 Starting demo..."
echo "   (Press Ctrl+C to stop)"
echo ""

cd "$PROJECT_ROOT"
$PYTHON_CMD examples/demo_sumo.py

echo ""
echo "Demo completed!"
