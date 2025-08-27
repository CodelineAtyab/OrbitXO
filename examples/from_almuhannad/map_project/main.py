from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import sys
import os
import datetime
import json
from typing import Optional, List, Dict, Any
from pathlib import Path

from googleApi import get_travel_time, load_locations_from_config
from minimum_time_tracking import check_and_notify_new_minimum
from logging_task import LoggingSystem
from db_helper import create_connection, add_travel_time_record, get_historical_data, get_minimum_travel_time

# Initialize FastAPI app
app = FastAPI(
    title="Travel Time API",
    description="API for tracking travel times between locations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

# Initialize logging
logger = LoggingSystem(app_name="MapProjectAPI")

# Pydantic models for request/response
class TravelTimeRequest(BaseModel):
    source: str
    destination: str
    use_mock_data: bool = False

class HistoricalDataRequest(BaseModel):
    source: str
    destination: str
    date: Optional[str] = None

class TravelTimeResponse(BaseModel):
    success: bool
    source: str
    destination: str
    distance: Optional[str] = None
    distance_value: Optional[int] = None
    duration: Optional[str] = None
    duration_minutes: Optional[int] = None
    minimum_time_info: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

def process_travel_time(source, destination, use_mock_data=False):
    """
    Process travel time data, store in database and check for minimum time
    Returns a dictionary with the results
    """
    logger.log_with_context('info', "Processing travel time", {"source": source, "destination": destination, "mock": use_mock_data})
    
    if use_mock_data:
        logger.log_with_context('info', "Using mock travel time data", {"source": source, "destination": destination})
        travel_result = {
            "success": True,
            "source": source,
            "destination": destination,
            "distance": "1012.5 km",
            "distance_value": 1012500,
            "duration": "10 hours 30 min",
            "duration_value": 37800
        }
    else:
        logger.log_with_context('info', "Requesting travel time from Google Maps API", {"source": source, "destination": destination})
        travel_result = get_travel_time(source, destination)
    
    if not travel_result["success"]:
        logger.log_with_context('error', "Failed to get travel time data", {"error": travel_result.get("error", "Unknown error")})
        return {
            "success": False,
            "source": source,
            "destination": destination,
            "error": travel_result.get("error", "Failed to get travel time data")
        }
    
    duration_minutes = travel_result["duration_value"] // 60
    
    logger.log_with_context('info', "Adding travel time record to database", {
        "source": source,
        "destination": destination,
        "duration_minutes": duration_minutes,
        "distance": travel_result["distance"]
    })
    
    add_travel_time_record(
        source=source,
        destination=destination,
        duration_minutes=duration_minutes,
        distance=travel_result["distance"],
        distance_value=travel_result.get("distance_value")
    )
    
    # Check if this is a minimum time
    logger.log_with_context('info', "Checking for minimum travel time", {"duration_minutes": duration_minutes})
    min_time_result = check_and_notify_new_minimum(source, destination, duration_minutes)
    
    return {
        "success": True,
        "source": source,
        "destination": destination,
        "distance": travel_result["distance"],
        "distance_value": travel_result.get("distance_value"),
        "duration": travel_result["duration"],
        "duration_minutes": duration_minutes,
        "minimum_time_info": min_time_result
    }

# Background task to process travel time asynchronously
def process_travel_time_task(source: str, destination: str, use_mock_data: bool = False):
    """Background task to process travel time data"""
    process_travel_time(source, destination, use_mock_data)

# API endpoints
@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint that serves the HTML UI"""
    logger.log_with_context('info', "Serving index.html", {"endpoint": "/"})
    
    # Read the HTML file
    html_file_path = Path(__file__).parent / "index.html"
    logger.log_with_context('debug', "HTML file path", {"path": str(html_file_path)})
    
    # Check if file exists first
    if not html_file_path.exists():
        error_msg = f"index.html not found at path: {str(html_file_path)}"
        logger.log_with_context('error', error_msg, {"path": str(html_file_path)})
        return HTMLResponse(
            content=f"<html><body><h1>Error: UI file not found</h1><p>{error_msg}</p></body></html>",
            status_code=500
        )
    
    try:
        with open(html_file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except Exception as e:
        error_msg = f"Error reading index.html: {str(e)}"
        logger.log_with_context('error', error_msg, {"path": str(html_file_path), "error": str(e)})
        return HTMLResponse(
            content=f"<html><body><h1>Error: Could not read UI file</h1><p>{error_msg}</p></body></html>",
            status_code=500
        )

@app.get("/api-info")
async def api_info():
    """Endpoint that returns API info"""
    return {
        "name": "Travel Time API",
        "version": "1.0.0",
        "description": "API for tracking travel times between locations"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for container monitoring"""
    try:
        # Test database connection
        connection = create_connection()
        if not connection:
            return JSONResponse(
                status_code=500,
                content={"status": "error", "message": "Database connection failed"}
            )
        connection.close()
        
        return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat()}
    except Exception as e:
        logger.log_with_context('error', "Health check failed", {"error": str(e)})
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.post("/travel-time", response_model=TravelTimeResponse)
async def get_travel_time_api(request: TravelTimeRequest):
    """Get travel time between source and destination"""
    logger.log_with_context('info', "API request: get travel time", {
        "source": request.source,
        "destination": request.destination,
        "mock": request.use_mock_data
    })
    
    result = process_travel_time(
        source=request.source,
        destination=request.destination,
        use_mock_data=request.use_mock_data
    )
    
    if not result["success"]:
        return JSONResponse(
            status_code=400,
            content=result
        )
    
    return result

@app.post("/travel-time/async", status_code=202)
async def get_travel_time_async(request: TravelTimeRequest, background_tasks: BackgroundTasks):
    """Submit travel time processing as a background task"""
    logger.log_with_context('info', "API request: get travel time async", {
        "source": request.source,
        "destination": request.destination
    })
    
    background_tasks.add_task(
        process_travel_time_task,
        source=request.source,
        destination=request.destination,
        use_mock_data=request.use_mock_data
    )
    
    return {
        "message": "Travel time processing submitted",
        "source": request.source,
        "destination": request.destination
    }

@app.get("/historical-data")
async def get_historical_data_api(
    source: str = Query(..., description="Source location"),
    destination: str = Query(..., description="Destination location"),
    date: Optional[str] = Query(None, description="Optional date filter (YYYY-MM-DD)")
):
    """Get historical travel time data"""
    logger.log_with_context('info', "API request: get historical data", {
        "source": source,
        "destination": destination,
        "date": date
    })
    
    data = get_historical_data(source, destination, date)
    
    return {
        "source": source,
        "destination": destination,
        "date": date,
        "records": data
    }

@app.get("/config")
async def get_config():
    """Get current configuration"""
    try:
        source, destination = load_locations_from_config()
        
        return {
            "source": source,
            "destination": destination
        }
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run a scheduled task on app startup
@app.on_event("startup")
async def startup_event():
    logger.log_with_context('info', "API startup", {"time": datetime.datetime.now().isoformat()})
    
    # Ensure database is initialized
    connection = create_connection()
    if connection:
        connection.close()

# Main entry point
if __name__ == "__main__":
    # Run the API with Uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )

def track_travel_time(source, destination, use_mock_data=False):
    logger = LoggingSystem(app_name="MapProject")
    
    if use_mock_data:
        logger.log_with_context('info', "Using mock travel time data", {"source": source, "destination": destination})
        travel_result = {
            "success": True,
            "source": source,
            "destination": destination,
            "distance": "1012.5 km",
            "distance_value": 1012500,
            "duration": "10 hours 30 min",
            "duration_value": 37800
        }
    else:
        logger.log_with_context('info', "Requesting travel time from Google Maps API", {"source": source, "destination": destination})
        travel_result = get_travel_time(source, destination)
    
    if not travel_result["success"]:
        logger.log_with_context('error', "Failed to get travel time data", {"error": travel_result.get("error", "Unknown error")})
        return None
    
    duration_minutes = travel_result["duration_value"] // 60
    
    logger.log_with_context('info', "Adding travel time record to database", {
        "source": source,
        "destination": destination,
        "duration_minutes": duration_minutes,
        "distance": travel_result["distance"]
    })
    
    add_travel_time_record(
        source=source,
        destination=destination,
        duration_minutes=duration_minutes,
        distance=travel_result["distance"],
        distance_value=travel_result.get("distance_value")
    )
    
    return {
        "travel_result": travel_result
    }

def main():
    # Initialize logging system
    logger = LoggingSystem(app_name="MapProject", log_dir=None)
    
    try:
        logger.log_with_context('info', "Starting travel time tracking", {"component": "main"})
        try:
            source, destination = load_locations_from_config()
            logger.log_with_context('info', "Loaded location configuration", {"source": source, "destination": destination})
        except ValueError as e:
            logger.log_with_context('error', "Failed to load location configuration", {"error": str(e)})
            return 1
        
        logger.log_with_context('info', "Requesting travel time data", {"source": source, "destination": destination})
        result = track_travel_time(source, destination)
        
        if not result:
            logger.log_with_context('warning', "Failed to get real travel time data, using mock data", {"source": source, "destination": destination})
            result = track_travel_time(source, destination, use_mock_data=True)
        
        if result:
            travel_result = result["travel_result"]
            duration_minutes = travel_result["duration_value"] // 60
            
            # Check if this is a minimum time and notify via Slack if needed
            logger.log_with_context('info', "Checking for minimum travel time", {"duration_minutes": duration_minutes})
            min_time_result = check_and_notify_new_minimum(source, destination, duration_minutes)
            
            if min_time_result["new_minimum"]:
                logger.log_with_context('info', "New minimum travel time detected", {
                    "previous_min": min_time_result["previous_min"],
                    "new_min": min_time_result["current_duration"],
                    "time_saved": min_time_result["time_saved"]
                })
            
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            get_historical_data(source, destination, today)
            logger.log_with_context('info', "Travel time tracking completed successfully")
            return 0
        else:
            logger.log_with_context('error', "Failed to get travel time data", {"source": source, "destination": destination})
            return 1
    
    except Exception as e:
        logger.log_with_context('critical', "Unexpected error in main function", {"error": str(e)})
        return 1

if __name__ == "__main__":
    sys.exit(main())
