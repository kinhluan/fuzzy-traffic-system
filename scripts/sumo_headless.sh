#!/bin/bash
# Run SUMO in headless mode (no GUI)
# Faster for batch simulations and benchmarking

set -e  # Exit on error

echo "========================================="
echo "  SUMO Headless Mode + Fuzzy Controller"
echo "========================================="
echo ""

# Determine script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DEMO_SCRIPT="$PROJECT_ROOT/examples/demo_sumo.py"

# Check if network exists
NETWORK_FILE="$PROJECT_ROOT/sumo_files/networks/single_intersection.net.xml"
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

echo "✓ Python available"
echo ""

# Modify demo_sumo.py to use headless mode
echo "🚀 Running in headless mode (no GUI)..."
echo "   This is faster for simulations"
echo ""

# Create temporary script with use_gui=False
TEMP_SCRIPT="/tmp/demo_sumo_headless.py"
cat "$DEMO_SCRIPT" | sed 's/use_gui=True/use_gui=False/' > "$TEMP_SCRIPT"

# Run demo
cd "$PROJECT_ROOT"
$PYTHON_CMD "$TEMP_SCRIPT"

# Cleanup
rm -f "$TEMP_SCRIPT"

echo ""
echo "Headless simulation completed!"
