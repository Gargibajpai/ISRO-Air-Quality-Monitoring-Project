#!/bin/bash

echo "========================================"
echo "   AirScan Lite - Air Quality Monitor"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

echo "Python version:"
python3 --version
echo

echo "Installing/updating dependencies..."
pip3 install -r requirements.txt

echo
echo "Starting AirScan Lite..."
echo "The application will open in your default web browser"
echo "If it doesn't open automatically, go to: http://localhost:8501"
echo
echo "Press Ctrl+C to stop the application"
echo

streamlit run app.py 