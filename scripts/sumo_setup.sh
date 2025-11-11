#!/bin/bash
# SUMO Network Setup Script
# Generates SUMO network files from XML definitions

set -e  # Exit on error

echo "========================================="
echo "  SUMO Network Setup"
echo "========================================="
echo ""

# Check if SUMO is installed
if ! command -v netconvert &> /dev/null; then
    echo "❌ ERROR: netconvert not found"
    echo ""
    echo "Please install SUMO first:"
    echo "  macOS:   brew install sumo"
    echo "  Ubuntu:  sudo apt install sumo sumo-tools"
    echo "  Windows: Download from https://sumo.dlr.de/docs/Downloads.php"
    exit 1
fi

# Check SUMO_HOME
if [ -z "$SUMO_HOME" ]; then
    echo "⚠️  WARNING: SUMO_HOME not set"
    echo "   Attempting to continue anyway..."
    echo ""
fi

# Navigate to network directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
NETWORK_DIR="$PROJECT_ROOT/sumo_files/networks"

echo "📂 Network directory: $NETWORK_DIR"
echo ""

# Check if network files exist
if [ ! -f "$NETWORK_DIR/single_intersection.nod.xml" ]; then
    echo "❌ ERROR: Node file not found: single_intersection.nod.xml"
    exit 1
fi

if [ ! -f "$NETWORK_DIR/single_intersection.edg.xml" ]; then
    echo "❌ ERROR: Edge file not found: single_intersection.edg.xml"
    exit 1
fi

if [ ! -f "$NETWORK_DIR/single_intersection.typ.xml" ]; then
    echo "❌ ERROR: Type file not found: single_intersection.typ.xml"
    exit 1
fi

echo "✓ Input files found"
echo ""

# Generate network
echo "🔨 Generating SUMO network..."
cd "$NETWORK_DIR"

netconvert \
    --node-files=single_intersection.nod.xml \
    --edge-files=single_intersection.edg.xml \
    --type-files=single_intersection.typ.xml \
    --output-file=single_intersection.net.xml \
    --no-turnarounds=true \
    --junctions.limit-turn-speed=5.5

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Network generated successfully!"
    echo "   Output: single_intersection.net.xml"
    echo ""
    echo "You can now run the demo:"
    echo "  ./scripts/sumo_run.sh"
else
    echo ""
    echo "❌ Network generation failed"
    exit 1
fi
