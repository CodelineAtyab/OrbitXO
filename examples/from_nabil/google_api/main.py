import os
import sys
from fastapi import FastAPI, Query, HTTPException, Depends, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import uvicorn

# Add the current directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Load environment variables
load_dotenv()

# Import your existing modules
from logging_implementation import root_logger as logger, set_debug_mode
from googleapi import get_travel_time, DEFAULT_SOURCE, DEFAULT_DESTINATION
from database_integration import get_database_connection, create_tables, record_travel_time

# Initialize FastAPI app
app = FastAPI(
    title="Travel Time API",
    description="API for getting travel time between locations using Google Maps API",
    version="1.0.0"
)

# Set up templates directory
templates = Jinja2Templates(directory=current_dir)

# Models for request and response
class TravelTimeRequest(BaseModel):
    source: str
    destination: str
    use_mock: Optional[bool] = False

class TravelTimeResponse(BaseModel):
    success: bool
    source: Optional[str] = None
    destination: Optional[str] = None
    distance: Optional[str] = None
    duration: Optional[str] = None
    error: Optional[str] = None
    details: Optional[str] = None
    mock_data: Optional[bool] = None

# Database dependency
def get_db():
    try:
        conn = get_database_connection()
        create_tables(conn)
        yield conn
        conn.close()
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Return the HTML file
    return templates.TemplateResponse("ui.html", {"request": request})

@app.get("/api")
def api_root():
    return {"message": "Travel Time API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/travel-time", response_model=TravelTimeResponse)
def calculate_travel_time(
    request: TravelTimeRequest,
    db=Depends(get_db)
):
    logger.info(f"Received travel time request from {request.source} to {request.destination}")
    
    try:
        # Get API key from environment
        api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
        if not api_key:
            logger.warning("No API key found in environment variables")
        
        # Get travel time
        result = get_travel_time(
            source=request.source, 
            destination=request.destination,
            api_key=api_key,
            use_mock=request.use_mock
        )
        
        if not result["success"]:
            logger.error(f"API Error: {result.get('error')}")
            return JSONResponse(
                status_code=400,
                content=result
            )
            
        # Record in database if successful
        if db and result.get("duration_value"):
            record_travel_time(
                db,
                request.source,
                request.destination,
                result["duration_value"] / 60  # Convert seconds to minutes
            )
            
        return result
        
    except Exception as e:
        logger.error(f"Error calculating travel time: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal server error",
                "details": str(e)
            }
        )

@app.get("/default-route", response_model=TravelTimeResponse)
def get_default_route(db=Depends(get_db)):
    """Get travel time for the default route defined in environment variables"""
    logger.info("Getting travel time for default route")
    
    try:
        # Get API key from environment
        api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
        
        # Get travel time for default route
        result = get_travel_time(
            source=DEFAULT_SOURCE,
            destination=DEFAULT_DESTINATION,
            api_key=api_key
        )
        
        if not result["success"]:
            logger.error(f"API Error: {result.get('error')}")
            return JSONResponse(
                status_code=400,
                content=result
            )
            
        # Record in database if successful
        if db and result.get("duration_value"):
            record_travel_time(
                db,
                DEFAULT_SOURCE,
                DEFAULT_DESTINATION,
                result["duration_value"] / 60  # Convert seconds to minutes
            )
            
        return result
        
    except Exception as e:
        logger.error(f"Error getting default route: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal server error",
                "details": str(e)
            }
        )

# Debug mode endpoint
@app.get("/debug", include_in_schema=False)
def toggle_debug():
    set_debug_mode()
    return {"message": "Debug mode enabled"}

if __name__ == "__main__":
    # Check for debug mode from environment
    if os.environ.get("DEBUG_MODE", "False").lower() == "true" or "--debug" in sys.argv:
        set_debug_mode()
        logger.debug("Debug mode enabled")
    
    # Start the FastAPI application
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    logger.info(f"Starting FastAPI application on {host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)