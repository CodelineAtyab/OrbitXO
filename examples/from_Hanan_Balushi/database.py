from logging_config import log_setup


log = log_setup("database")

def store_travel_time(record):
    log.info("Connecting to database")
    log.info(f"Storing new travel time record: {record}")