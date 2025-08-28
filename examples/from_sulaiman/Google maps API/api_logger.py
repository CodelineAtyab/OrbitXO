import logging
import os
from distance_matrix import get_distance_matrix
import json

# Configure basic logging to a file
logging.basicConfig(filename='api2_logger.logs', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_distance_matrix():
    try:
        # Get API key from environment variable
        API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
        
        # Example usage
        origins = ["Seattle, WA"]
        destinations = ["San Francisco, CA", "Portland, OR"]
        
        logger.info(f"Requesting distance matrix from {origins} to {destinations}")
        result = get_distance_matrix(origins, destinations, API_KEY)
        
        # Log the result summary
        if result.get("status") == "OK":
            logger.info("Distance matrix request successful")
            for i, origin in enumerate(result["origin_addresses"]):
                for j, destination in enumerate(result["destination_addresses"]):
                    element = result["rows"][i]["elements"][j]
                    if element["status"] == "OK":
                        logger.info(f"From {origin} to {destination}: Distance: {element['distance']['text']}, Duration: {element['duration']['text']}")
                    else:
                        logger.error(f"From {origin} to {destination}: Error: {element['status']}")
        else:
            logger.error(f"Distance matrix request failed: {result.get('error_message', 'Unknown error')}")
            
        return result
    except Exception as e:
        logger.error(f"Exception occurred while running distance matrix: {str(e)}")
        raise

if __name__ == "__main__":
    logger.info("Starting distance matrix application")
    result = run_distance_matrix()
    logger.info("Distance matrix application completed")
    
    # Pretty print the result for console output
    print(json.dumps(result, indent=2))