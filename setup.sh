#!/bin/bash

# Trinity Hostel Management System - Setup Script (macOS/Linux)
# This script sets up the virtual environment and dependencies

echo ""
echo "========================================"
echo "Trinity Hostel Management System"
echo "Setup Script for macOS/Linux"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "[1/5] Python found. Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2/5] Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "[3/5] Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[4/5] Running database migrations..."
python manage.py migrate

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to run migrations"
    exit 1
fi

echo "[5/5] Loading initial data..."
python manage.py loaddata fixtures/initial_data.json

if [ $? -ne 0 ]; then
    echo "WARNING: Failed to load fixtures (this is optional)"
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To run the development server:"
echo ""
echo "  1. Activate virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the server:"
echo "     python manage.py runserver"
echo ""
echo "  3. Open browser to:"
echo "     http://localhost:8000"
echo ""
echo "To create a superuser (admin account):"
echo "  python manage.py createsuperuser"
echo ""
