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

# Check for Docker availability
try:
    import docker
    DOCKER_AVAILABLE = True
    logger.info("Docker SDK is available")
except ImportError:
    DOCKER_AVAILABLE = False
    logger.warning("Docker SDK is not available. MySQL features may not work correctly.")

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
    
class DatabaseStatusResponse(BaseModel):
    database_connected: bool
    message: str

# Explicitly load .env file
from dotenv import load_dotenv, find_dotenv
dotenv_path = find_dotenv()
if dotenv_path:
    print(f"Loading environment from: {dotenv_path}")
    load_dotenv(dotenv_path)
else:
    print("Warning: .env file not found!")

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
        
        # First, make sure MySQL is running
        from db_logger import start_mysql_container
        mysql_ready = start_mysql_container()
        if not mysql_ready:
            logger.error("Failed to start MySQL container")
            return RouteResponse(
                success=False,
                message="Failed to start MySQL database. Please run start_mysql.bat first."
            )
        
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

@app.get("/api/database-status", response_model=DatabaseStatusResponse)
async def get_database_status():
    """Check if the MySQL database connection is working"""
    try:
        from db_logger import create_db_connection
        
        # Try to connect to the database
        connection = create_db_connection()
        
        if connection:
            # Connection successful
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()[0]
            cursor.close()
            connection.close()
            
            logger.info(f"Database connection successful. MySQL version: {version}")
            return DatabaseStatusResponse(
                database_connected=True,
                message=f"Connected to MySQL version: {version}"
            )
        else:
            # Connection failed
            logger.error("Failed to connect to MySQL database")
            return DatabaseStatusResponse(
                database_connected=False,
                message="Failed to connect to MySQL database. Check if Docker and MySQL container are running."
            )
    except Exception as e:
        logger.error(f"Error checking database connection: {str(e)}")
        return DatabaseStatusResponse(
            database_connected=False,
            message=f"Error: {str(e)}"
        )

@app.post("/api/start-mysql")
async def start_mysql():
    """Start the MySQL container if it's not running"""
    try:
        from db_logger import start_mysql_container
        
        # Try to start the MySQL container
        success = start_mysql_container()
        
        if success:
            logger.info("MySQL container started successfully")
            return JSONResponse(
                content={"success": True, "message": "MySQL container started successfully"},
                status_code=200
            )
        else:
            logger.error("Failed to start MySQL container")
            return JSONResponse(
                content={"success": False, "message": "Failed to start MySQL container. Check logs for details."},
                status_code=500
            )
    except Exception as e:
        logger.error(f"Error starting MySQL container: {str(e)}")
        return JSONResponse(
            content={"success": False, "message": f"Error: {str(e)}"},
            status_code=500
        )

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI application")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
