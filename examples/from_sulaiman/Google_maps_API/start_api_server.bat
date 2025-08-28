@echo off
echo Starting Google Maps Route Tracker API...
echo.
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
pause
