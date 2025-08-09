#!/bin/bash
"""
Setup script for the Tic-Tac-Toe API.

This script sets up the environment and starts the API server.
"""

echo "=== Tic-Tac-Toe API Setup ==="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "Error: pip is required but not installed."
    exit 1
fi

echo "Installing dependencies..."
pip install -r requirements.txt

echo
echo "Starting the API server..."
echo "The API will be available at http://localhost:8000"
echo "API documentation will be available at http://localhost:8000/docs"
echo
echo "Press Ctrl+C to stop the server"
echo

# Start the server
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000