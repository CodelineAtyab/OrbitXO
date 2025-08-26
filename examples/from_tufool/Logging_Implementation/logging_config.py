# logging_config.py

import logging
from logging.handlers import TimedRotatingFileHandler
import os

def setup_logging():
    LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
    LOG_FILE = os.path.join(LOG_DIR, "app.log")
    os.makedirs(LOG_DIR, exist_ok=True)  # Ensure logs directory exists

    file_handler = TimedRotatingFileHandler(
        LOG_FILE, when="midnight", interval=1, backupCount=7, encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    ))

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    ))

    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, stream_handler]
    )
    # Optional: also log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
