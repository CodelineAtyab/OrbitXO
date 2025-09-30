import logging
from datetime import datetime
import os


def setup_api_logger():
    """Set up and configure the API logger for file logging."""
    
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Create logger
    logger = logging.getLogger('api_logger')
    logger.setLevel(logging.INFO)
    
    # Create file handler
    log_filename = os.path.join(logs_dir, f"api_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Add formatter to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    if not logger.handlers:  # Avoid adding handlers multiple times
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


# Create the logger instance
api_logger = setup_api_logger()