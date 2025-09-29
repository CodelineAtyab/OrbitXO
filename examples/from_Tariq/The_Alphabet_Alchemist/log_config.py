import logging
from logging.handlers import TimedRotatingFileHandler
import os

# Create a logs directory if it doesn't exist
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, "api.log")

# Get the logger
api_logger = logging.getLogger("api_logger")
api_logger.setLevel(logging.INFO)

# Create a handler that rotates the log file every Monday
# It will keep one backup file (the previous week's log)
handler = TimedRotatingFileHandler(
    LOG_FILE, 
    when="W0",  # W0 means Monday
    interval=1, 
    backupCount=1
)

# Create a formatter and set it for the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
if not api_logger.handlers:
    api_logger.addHandler(handler)