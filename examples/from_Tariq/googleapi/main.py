from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
import sys
import os
import dotenv
from pydantic import BaseModel

# Import your existing modules
from googlemapapi import get_travel_time
import timetracker
import Logging_Implementation
from connection_module import get_db_connector

# Initialize FastAPI
app = FastAPI(
    title="Travel Time Tracker API",
    description="API for tracking travel times between locations using Google Maps",
    version="1.0.0"
)

# Set up static files and templates
# Create a 'static' directory for CSS, JS, etc. if needed
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(static_dir, exist_ok=True)

# Mount static directory if you need to serve static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

def get_logger():
    return Logging_Implementation.get_app_logger("travel_tracker")

def get_api_logger():
    return Logging_Implementation.get_api_logger("google_maps")

# Setup environment on startup (reusing your existing function)
@app.on_event("startup")
def startup_event():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    logs_dir = os.path.join(base_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    os.environ["LOGS_DIR"] = logs_dir
    
    logger = Logging_Implementation.get_app_logger("fastapi")
    logger.info(f"Logs directory set to: {logs_dir}")
    
    env_path = os.path.join(base_dir, ".env")
    if os.path.exists(env_path):
        dotenv.load_dotenv(env_path)
        logger.info(f"Loaded environment from {env_path}")
    else:
        logger.error(f"Environment file not found at {env_path}")
        raise Exception("Environment file not found")

# Serve UI.html at root
@app.get("/", response_class=HTMLResponse)
async def get_ui():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "UI.html"), "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/default-locations")
def get_default_locations():
    """Get default source and destination from environment variables"""
    source = os.environ.get("SOURCE")
    destination = os.environ.get("DESTINATION")
    
    if not source or not destination:
        raise HTTPException(status_code=404, detail="Default locations not configured")
    
    return {"source": source, "destination": destination}

# Add this model
class LocationRequest(BaseModel):
    source: str
    destination: str

# Replace the track_travel_time function with this
@app.post("/track-travel-time")
def track_travel_time(
    location_data: LocationRequest,
    logger=Depends(get_logger), 
    api_logger=Depends(get_api_logger)
):
    """Track travel time between specified locations"""
    source = location_data.source
    destination = location_data.destination
    
    logger.info(f"Getting travel time from {source} to {destination}")
    
    api_logger.debug(f"Making Google Maps API call for {source} to {destination}")
    travel_result = get_travel_time(source, destination)
    
    if not travel_result["success"]:
        api_logger.error(f"Failed to get travel time: {travel_result['error']}")
        api_logger.debug(f"Error details: {travel_result.get('details', 'No details provided')}")
        raise HTTPException(status_code=500, detail=f"Google Maps API error: {travel_result['error']}")
    else:
        api_logger.info(f"Successful API response received")
        api_logger.debug(f"API response: {travel_result}")
    
    duration_minutes = travel_result["duration_value"] // 60
    
    logger.info(f"Travel time: {travel_result['duration']} ({duration_minutes} minutes)")
    logger.info(f"Distance: {travel_result['distance']}")
    
    db = get_db_connector()
    is_recorded = db["add_travel_time_record"](
        source=source,
        destination=destination,
        duration_minutes=duration_minutes,
        distance=travel_result["distance"],
        distance_value=travel_result.get("distance_value")
    )
    
    if is_recorded:
        logger.info("Travel time recorded in database")
    else:
        logger.warning("Failed to record travel time in database")
    
    logger.info("Checking if this is a new minimum travel time...")
    tracker_result = timetracker.check_and_notify_new_minimum(source, destination, duration_minutes)
    
    if tracker_result["new_minimum"]:
        logger.info(f"New minimum travel time detected: {tracker_result['current_duration']} minutes")
        logger.info(f"Previous minimum: {tracker_result['previous_min']} minutes")
        logger.info(f"Time saved: {tracker_result['time_saved']} minutes")
    
    return {
        "travel_result": travel_result,
        "tracker_result": tracker_result
    }

@app.post("/track-default-locations")
async def track_default_locations(background_tasks: BackgroundTasks):
    """Track travel time using default locations from environment variables"""
    source = os.environ.get("SOURCE")
    destination = os.environ.get("DESTINATION")
    
    if not source or not destination:
        raise HTTPException(status_code=404, detail="Default locations not configured")
    
    # Run tracking in a background task to avoid blocking the response
    background_tasks.add_task(track_travel_time, source, destination)
    
    return {"message": "Travel time tracking started in background", "source": source, "destination": destination}

@app.get("/track-now")
def track_now():
    """Immediately track travel time using default locations and return results"""
    source = os.environ.get("SOURCE")
    destination = os.environ.get("DESTINATION")
    
    if not source or not destination:
        raise HTTPException(status_code=404, detail="Default locations not configured")
    
    # This will block until complete, but will return full results
    result = track_travel_time(source, destination)
    
    return result

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)