import sys
import uvicorn
import os
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Optional
import logging
from logging.handlers import RotatingFileHandler
from measurement_converter import MeasurementConverter
from database_manager import DatabaseManager

# Read version from version.txt
VERSION = "1.0.0"
try:
    if os.path.exists('version.txt'):
        with open('version.txt', 'r') as f:
            VERSION = f.read().strip()
except Exception:
    pass

# Setup logging
os.makedirs('logs', exist_ok=True)
logger = logging.getLogger('measurement_api')
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# File handler with rotation (1 week of logs)
file_handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10*1024*1024,  # 10MB per file
    backupCount=7  # Keep 7 days of logs
)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

app = FastAPI(title="Package Measurement Conversion API", version=VERSION)

# Initialize components
converter = MeasurementConverter()
db_manager = DatabaseManager()

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info("Application starting up...")
    db_manager.initialize_database()
    logger.info("Database initialized successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Application shutting down...")
    db_manager.close()

@app.get("/changelog")
async def get_changelog():
    """
    Retrieve the changelog content
    """
    logger.info("Changelog endpoint accessed")
    
    # Debug: Check current working directory and files
    import os
    cwd = os.getcwd()
    files = os.listdir(cwd)
    logger.info(f"Current working directory: {cwd}")
    logger.info(f"Files in directory: {files}")
    
    try:
        changelog_path = 'CHANGELOG.md'
        abs_path = os.path.abspath(changelog_path)
        logger.info(f"Looking for changelog at: {abs_path}")
        logger.info(f"File exists: {os.path.exists(changelog_path)}")
        
        if os.path.exists(changelog_path):
            with open(changelog_path, 'r') as f:
                changelog_content = f.read()
            logger.info("Changelog file found and read successfully")
            return {
                "version": VERSION,
                "changelog": changelog_content
            }
        else:
            logger.warning(f"Changelog file not found at {changelog_path}")
            # Return a default changelog if file doesn't exist
            return {
                "version": VERSION,
                "changelog": "",
                "note": "Using default changelog - CHANGELOG.md file not found in container",
                "debug_info": {
                    "cwd": cwd,
                    "files_in_directory": files,
                    "abs_path": abs_path
                }
            }
    except Exception as e:
        logger.error(f"Failed to read changelog: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": f"Failed to retrieve changelog: {str(e)}",
                "version": VERSION
            }
        )

@app.get("/convert-measurements")
async def convert_measurements(
    input_string: str = Query(..., alias="convert-measurements", description="Measurement input string to convert")
):
    """
    Convert measurement input string into a list of total values for each package.
    
    Rules:
    - 'z' cannot stand alone, must be with another character
    - '_' (underscore) = 0
    - 'a' to 'y' = 1 to 25 (note: 'z' is special, not 26)
    - Multiple characters are added together for numbers > 25
    """
    logger.info(f"Conversion request received: {input_string}")
    
    try:
        result = converter.convert(input_string)
        
        # Store in database
        db_manager.save_conversion(input_string, result)
        
        logger.info(f"Conversion successful: {input_string} -> {result}")
        
        return JSONResponse(
            status_code=200,
            content={
                "input": input_string,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        )
    except Exception as e:
        logger.error(f"Conversion failed for input '{input_string}': {str(e)}")
        return JSONResponse(
            status_code=400,
            content={
                "error": str(e),
                "input": input_string
            }
        )

@app.get("/history")
async def get_history(limit: Optional[int] = Query(100, description="Maximum number of records to retrieve")):
    """
    Retrieve conversion history from the database.
    """
    logger.info(f"History request received with limit: {limit}")
    
    try:
        history = db_manager.get_history(limit)
        logger.info(f"Retrieved {len(history)} history records")
        
        return JSONResponse(
            status_code=200,
            content={
                "count": len(history),
                "history": history
            }
        )
    except Exception as e:
        logger.error(f"Failed to retrieve history: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e)
            }
        )

if __name__ == "__main__":
    port = 8080
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)