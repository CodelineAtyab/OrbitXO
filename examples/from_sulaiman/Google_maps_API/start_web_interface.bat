@echo off
echo Starting Google Maps Route Tracking Web Interface...

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not found in your PATH. Please install Python first.
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking requirements...
pip install -r requirements.txt

REM Run the web application
echo Starting web server...
echo.
echo Access the web interface at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
python app.py

pause
