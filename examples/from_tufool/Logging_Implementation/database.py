import logging

def save_travel_time(response):
    logging.info("Connecting to database")
    logging.info(f"Storing new travel time record: {response['duration']}")
