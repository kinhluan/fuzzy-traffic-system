#!/bin/bash
# Open SUMO-GUI directly (without fuzzy controller)
# Useful for testing network and routes

set -e  # Exit on error

echo "========================================="
echo "  SUMO-GUI Manual Mode"
echo "========================================="
echo ""

# Check if SUMO is installed
if ! command -v sumo-gui &> /dev/null; then
    echo "❌ ERROR: sumo-gui not found"
    echo ""
    echo "Please install SUMO first:"
    echo "  macOS:   brew install sumo"
    echo "  Ubuntu:  sudo apt install sumo sumo-tools"
    exit 1
fi

echo "✓ SUMO-GUI found"
echo ""

# Determine paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$PROJECT_ROOT/sumo_files/configs/single_intersection.sumocfg"

# Check if config exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ ERROR: Config file not found!"
    echo "   Expected: $CONFIG_FILE"
    exit 1
fi

echo "📄 Config: $CONFIG_FILE"
echo ""
echo "🚀 Opening SUMO-GUI..."
echo ""
echo "Controls:"
echo "  Space       - Start/Pause simulation"
echo "  Ctrl+A      - Fit view"
echo "  Mouse wheel - Zoom"
echo "  Right-drag  - Pan"
echo ""

# Open SUMO-GUI
sumo-gui -c "$CONFIG_FILE"

echo ""
echo "SUMO-GUI closed"
