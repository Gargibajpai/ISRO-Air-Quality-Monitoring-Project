@echo off
echo ========================================
echo    AirScan Lite - Air Quality Monitor
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

echo Installing/updating dependencies...
pip install -r requirements.txt

echo.
echo Starting AirScan Lite...
echo The application will open in your default web browser
echo If it doesn't open automatically, go to: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

streamlit run app.py

pause 