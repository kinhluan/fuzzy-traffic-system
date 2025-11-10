#!/bin/bash
# Test script - Run all system tests

set -e

echo "=================================================="
echo "  Fuzzy Traffic System - Running Tests"
echo "=================================================="
echo

# Run system test
echo "🧪 Running system tests..."
echo
poetry run python test_system.py

echo
echo "=================================================="
echo "✅ All tests passed!"
echo "=================================================="
