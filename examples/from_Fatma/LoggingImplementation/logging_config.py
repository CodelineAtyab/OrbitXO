import logging
import logging.handlers
import os

# -------- Settings --------
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Log format: timestamp, level, module, message
LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Configure root logger
logging.basicConfig(
    level=logging.DEBUG,  # capture DEBUG and above
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[
        logging.handlers.TimedRotatingFileHandler(
            filename=LOG_FILE,
            when="midnight",    # rotate daily
            interval=1,
            backupCount=7,      # keep 7 days of logs
            encoding="utf-8"
        ),
        logging.StreamHandler()  # also print logs to console
    ]
)

# Function to get a named logger for any module
def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
