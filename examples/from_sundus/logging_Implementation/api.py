
import logging
import time
logger = logging.getLogger("api")

def get_travel_time(source: str, destination: str) -> int:
    logger.info("Starting API request to Google Maps")
    logger.debug("Request parameters: {source: %r, destination: %r}", source, destination)
    # Simulate call
    time.sleep(0.1)
    # Simulate response
    status_code = 200
    logger.info("Received response: %s %s", status_code, "OK")
    # Pretend API says 26 minutes
    return 26
