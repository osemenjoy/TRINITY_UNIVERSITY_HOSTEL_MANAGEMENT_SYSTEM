@echo off
REM Trinity Hostel Management System - Setup Script (Windows)
REM This script sets up the virtual environment and dependencies

echo.
echo ========================================
echo Trinity Hostel Management System
echo Setup Script for Windows
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Python found. Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [3/5] Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/5] Running database migrations...
python manage.py migrate

if errorlevel 1 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)

echo [5/5] Loading initial data...
python manage.py loaddata fixtures/initial_data.json

if errorlevel 1 (
    echo WARNING: Failed to load fixtures (this is optional)
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the development server:
echo.
echo   1. Activate virtual environment:
echo      .\venv\Scripts\activate.bat
echo.
echo   2. Run the server:
echo      python manage.py runserver
echo.
echo   3. Open browser to:
echo      http://localhost:8000
echo.
echo To create a superuser (admin account):
echo   python manage.py createsuperuser
echo.
pause
