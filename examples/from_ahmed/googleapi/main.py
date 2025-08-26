from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from loginImplemenation import (
    get_api_logger, get_db_logger, get_app_logger,
    log_api_call, log_db_operation
)
from pydantic import BaseModel
import os
from googlemapapi import get_travel_time
import json
from datetime import datetime

app = FastAPI()

class LocationRequest(BaseModel):
    source: str
    destination: str

class TravelTimeRecord(BaseModel):
    source: str
    destination: str
    duration: int
    distance: int

@app.get("/", response_class=HTMLResponse)
def root():
    html_path = os.path.join(os.path.dirname(__file__), "ui.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/calculate")
def calculate_travel_time(request: LocationRequest):
    """Get real travel time using Google Maps API"""
    api_logger = get_api_logger("googlemaps")
    
    try:
        # Log the API call
        log_api_call(
            api_logger,
            method="POST",
            url="https://routes.googleapis.com/directions/v2:computeRoutes",
            params=None,
            headers={"User-Agent": "OrbitXO"},
            response=None,
            error=None
        )
        
        # Get the actual travel time from Google Maps API
        result = get_travel_time(request.source, request.destination)
        
        # Log the successful API call
        log_api_call(
            api_logger,
            method="POST",
            url="https://routes.googleapis.com/directions/v2:computeRoutes",
            params=None,
            headers={"User-Agent": "OrbitXO"},
            response=type('Response', (), {"status_code": 200, "elapsed": "120ms"})(),
            error=None
        )
        
        return {
            "duration": result["duration_minutes"],
            "distance": result["distance_km"],
            "status": "success"
        }
    except Exception as e:
        # Log the error
        log_api_call(
            api_logger,
            method="POST",
            url="https://routes.googleapis.com/directions/v2:computeRoutes",
            params=None,
            headers={"User-Agent": "OrbitXO"},
            response=None,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/log/db")
def log_db(record: TravelTimeRecord):
    db_logger = get_db_logger("travel_times")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # Here you would actually insert into your database
        # For now, we're just logging it
        log_db_operation(
            db_logger,
            operation="INSERT",
            table="travel_times",
            query="INSERT INTO travel_times (timestamp, source, destination, duration, distance) VALUES (?, ?, ?, ?, ?)",
            params=(timestamp, record.source, record.destination, record.duration, record.distance),
            result=[{"id": 1, "duration": record.duration}],
            error=None
        )
        return {"status": "Travel time recorded in database", "timestamp": timestamp}
    except Exception as e:
        log_db_operation(
            db_logger,
            operation="INSERT",
            table="travel_times",
            query="INSERT INTO travel_times (timestamp, source, destination, duration, distance) VALUES (?, ?, ?, ?, ?)",
            params=(timestamp, record.source, record.destination, record.duration, record.distance),
            result=None,
            error=str(e)
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/log/app")
def log_app():
    app_logger = get_app_logger("notifier")
    app_logger.warning("Failed to send Slack notification, retrying...")
    app_logger.info("Slack notification sent successfully")
    return {"status": "App log recorded"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
