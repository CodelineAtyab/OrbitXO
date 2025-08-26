import logging

def call_google_maps_api(source, destination):
    logging.info("Starting API request to Google Maps")
    logging.debug(f"Request parameters: {{source: '{source}', destination: '{destination}'}}")

    # Simulate response
    response = {"status": 200, "duration": "26 minutes"}

    logging.info("Received response: 200 OK")
    return response
