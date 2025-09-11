from logging_config import get_logger
db_logger = get_logger("database")

def store_record():
    db_logger.info("Connecting to database")
    db_logger.info("Storing new travel time record: 26 minutes")
