import sys
import os
import json
from dotenv import load_dotenv

# Add the current directory to the path to allow relative imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Load environment variables
load_dotenv()

# Use relative imports for files in the same directory
from logging_implementation import root_logger as logger, set_debug_mode
from googleapi import get_travel_time, DEFAULT_SOURCE, DEFAULT_DESTINATION


def main(): 
    logger.info("Application starting")
    
    # Check for debug mode from environment or command line
    if os.environ.get("DEBUG_MODE", "False").lower() == "true" or "--debug" in sys.argv:
        set_debug_mode()
        logger.debug("Debug mode enabled")
        
    try:
        # Get API key from environment
        api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
        if api_key:
            logger.info("Loaded API key from environment variables")
        else:
            logger.warning("No API key found in environment variables")
        
        # Get source and destination from environment variables
        source = DEFAULT_SOURCE
        destination = DEFAULT_DESTINATION
                    
        logger.info(f"Requesting directions from {source} to {destination}")
        directions = get_travel_time(source, destination, api_key=api_key)
        
        if not directions["success"]:
            logger.error(f"API Error: {directions['error']}")
            logger.error(f"API Error details: {directions.get('details', 'No additional details')}")
            return 1
            
        travel_time = directions["duration"]
        
        # Check if the result is using mock data
        if directions.get("mock_data", False):
            logger.warning("Using mock travel time data instead of actual API data")
            logger.warning("To get real data, please configure a valid Google Maps API key")
            
        logger.info(f"Retrieved travel time: {travel_time}")
        
        
        logger.info("Sending notifications")
        
        logger.info("Application completed successfully")
        return 0
        
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
