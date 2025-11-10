#!/bin/bash
# Clean script - Remove generated files and caches

set -e

echo "=================================================="
echo "  Fuzzy Traffic System - Clean"
echo "=================================================="
echo
echo "Removing generated files and caches..."
echo

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

# Remove pytest cache
rm -rf .pytest_cache 2>/dev/null || true

# Remove generated data (optional - uncomment if needed)
# rm -f web/data/comparison_results.json 2>/dev/null || true

echo "✓ Python cache cleaned"
echo "✓ Pytest cache cleaned"
echo
echo "=================================================="
echo "✅ Clean complete!"
echo "=================================================="
