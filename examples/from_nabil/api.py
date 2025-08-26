

import requests
import time
from examples.from_nabil.google_api.logging_implementation import api_logger as logger, LogContext

def make_api_request(url, params=None):

    logger.info(f"Starting API request to {url}")
    
    if params:
        logger.debug(f"Request parameters: {params}")
    
    try:
        with LogContext(logger, f"Request-{int(time.time())}"):
            start_time = time.time()
            response = requests.get(url, params=params)
            duration = time.time() - start_time
            
            logger.info(f"Received response: {response.status_code} {response.reason}")
            logger.debug(f"Response time: {duration:.2f} seconds")
            
            if response.status_code != 200:
                logger.warning(f"Unexpected status code: {response.status_code}")
                logger.debug(f"Response headers: {dict(response.headers)}")
                logger.debug(f"Response content: {response.text[:500]}...")
            
            return response.json()
    except requests.RequestException as e:
        logger.error(f"API request failed: {e}", exc_info=True)
        raise
def get_directions(source, destination):

    logger.info(f"Getting directions from {source} to {destination}")

    params = {
        "source": source,
        "destination": destination,
        "mode": "driving"
    }
    
    time.sleep(1)  
    
    logger.info("Directions retrieved successfully")
    return {
        "distance": "15 km",
        "duration": "26 minutes",
        "route": "Main St → Broadway → Park Ave"
    }

if __name__ == "__main__":
    directions = get_directions("home", "work")
    logger.info(f"Travel time: {directions['duration']}")
