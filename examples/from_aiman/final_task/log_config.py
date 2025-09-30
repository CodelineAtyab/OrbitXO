import logging
from logging.handlers import TimedRotatingFileHandler
import os

def setup_api_logger():
    """Configures and returns a logger that rotates weekly."""
    
    log_directory = "logs"
    log_file = os.path.join(log_directory, "api.log")

    # Create the logs directory if it does not exist.
    os.makedirs(log_directory, exist_ok=True)

    # Configure the logger.
    logger = logging.getLogger("api_logger")
    logger.setLevel(logging.INFO)

    # Add a handler only if one doesn't exist to prevent duplicate logs.
    if not logger.handlers:
        # The handler rotates the log file every Monday, keeping one backup.
        handler = TimedRotatingFileHandler(
            log_file, 
            when="W0",  # Monday
            interval=1, 
            backupCount=1
        )
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

# Create a logger instance for other modules to import.
api_logger = setup_api_logger()