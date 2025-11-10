#!/bin/bash
# Setup script - Install dependencies and prepare environment

set -e

echo "=================================================="
echo "  Fuzzy Traffic System - Setup"
echo "=================================================="
echo

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "❌ Poetry is not installed!"
    echo "   Please install Poetry first: https://python-poetry.org/docs/#installation"
    exit 1
fi

echo "✓ Poetry found: $(poetry --version)"
echo

# Install dependencies
echo "📦 Installing dependencies..."
poetry install
echo "✓ Dependencies installed"
echo

# Activate virtual environment
echo "🔧 Virtual environment ready at: .venv/"
echo
echo "To activate the environment, run:"
echo "  poetry shell"
echo
echo "✅ Setup complete!"
echo
echo "Next steps:"
echo "  1. poetry shell          # Activate environment"
echo "  2. ./scripts/test.sh     # Run tests"
echo "  3. ./scripts/run.sh      # Run simulation"
echo "=================================================="
