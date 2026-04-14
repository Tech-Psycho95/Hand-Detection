@echo off
REM Setup script for Hand Detection project

echo.
echo ========================================
echo Hand Detection Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org
    pause
    exit /b 1
)

echo [1/3] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/3] Verifying installation...
python -c "import cv2, mediapipe, playsound; print('All dependencies OK!')"
if errorlevel 1 (
    echo Warning: Some dependencies may not be properly installed
)

echo.
echo [3/3] Setup complete!
echo.
echo Next steps:
echo 1. Place your audio file as 'custom_voice.mp3' in this directory
echo 2. Run: python hand_detector.py
echo.
pause
