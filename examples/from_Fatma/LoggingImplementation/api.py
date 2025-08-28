from logging_config import get_logger
api_logger = get_logger("api")

def call_google_maps():
    api_logger.info("Starting API request to Google Maps")
    api_logger.debug('Request parameters: {source: "home", destination: "work"}')
    api_logger.info("Received response: 200 OK")