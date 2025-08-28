"""
FastAPI backend for Google Maps Route Tracking System
This API serves as the backend for the route tracking system frontend.
"""
import os
import sys
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

# Add the current directory to the path to import main.py modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import functions from main.py
from main import run_complete_system, setup_environment, run_route_tracker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/api.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("api")

# Create directories if they don't exist
if not os.path.exists('logs'):
    os.makedirs('logs')
    logger.info("Created logs directory")

# Initialize FastAPI app
app = FastAPI(
    title="Google Maps Route Tracker API",
    description="API for tracking routes between locations using Google Maps API",
    version="1.0.0"
)

# Configure CORS to allow requests from any origin (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class RouteRequest(BaseModel):
    origin: str
    destination: str
    continuous: bool = False
    interval: int = 300
    slack_notify: bool = True

class RouteResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

class ApiStatusResponse(BaseModel):
    api_configured: bool

# Setup environment at startup
setup_environment()

# Routes
@app.get("/", response_class=FileResponse)
async def read_root():
    """Serve the index.html file"""
    return FileResponse("static/index.html")

@app.get("/api/status", response_model=ApiStatusResponse)
async def get_api_status():
    """Check if the Google Maps API key is configured"""
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    return ApiStatusResponse(api_configured=bool(api_key))

@app.post("/api/track-route", response_model=RouteResponse)
async def track_route(origin: str = Form(...), destination: str = Form(...)):
    """API endpoint to track a route between two locations"""
    try:
        if not origin or not destination:
            raise HTTPException(status_code=400, detail="Both origin and destination are required")
        
        logger.info(f"API request to track route from {origin} to {destination}")
        
        # Call the main system
        result = run_complete_system(
            origin=origin,
            destination=destination,
            continuous=False,
            interval=300,
            slack_notify=True
        )
        
        if result:
            # Get route data from the tracker
            from route_tracker import RouteTracker
            tracker = RouteTracker(origin=origin, destination=destination)
            route_data = tracker.check_route()
            
            if route_data:
                return RouteResponse(
                    success=True,
                    message="Route tracked successfully",
                    data={
                        "origin": route_data['origin'],
                        "destination": route_data['destination'],
                        "distance": route_data['distance_text'],
                        "distance_meters": route_data['distance_meters'],
                        "duration": route_data['duration_text'],
                        "duration_seconds": route_data['duration_seconds'],
                        "is_min_distance": route_data['is_min_distance'],
                        "is_min_duration": route_data['is_min_duration'],
                        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                )
            else:
                return RouteResponse(
                    success=False,
                    message="Route tracking completed but no data was returned"
                )
        else:
            return RouteResponse(
                success=False,
                message="Failed to track route. Check logs for details."
            )
    
    except Exception as e:
        logger.error(f"Error processing route tracking request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI application")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
