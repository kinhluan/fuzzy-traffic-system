#!/bin/bash
# Serve script - Start local web server for dashboard

set -e

PORT=${1:-8000}

echo "=================================================="
echo "  Fuzzy Traffic System - Web Dashboard"
echo "=================================================="
echo
echo "Starting local web server..."
echo "Dashboard URL: http://localhost:$PORT"
echo
echo "Press Ctrl+C to stop the server"
echo "=================================================="
echo

cd web
python3 -m http.server $PORT
