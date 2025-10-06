import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Log file configuration
LOG_FILE = LOGS_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.INFO

def setup_logger(name: str = "measurement_converter") -> logging.Logger:
    """
    Configure and return a logger instance with both file and stream handlers.
    
    Args:
        name: The name of the logger (default: 'measurement_converter')
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Prevent adding handlers multiple times
    if not logger.handlers:
        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE,
            maxBytes=10_000_000,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(console_handler)

    return logger

def get_logger(name: str = "measurement_converter") -> logging.Logger:
    """
    Get or create a logger with the given name.
    
    Args:
        name: The name of the logger (default: 'measurement_converter')
    
    Returns:
        logging.Logger: Logger instance
    """
    return setup_logger(name)

# Create a default logger instance
logger = get_logger()

# Log levels convenience functions
def debug(msg: str, *args, **kwargs) -> None:
    """Log a debug message."""
    logger.debug(msg, *args, **kwargs)

def info(msg: str, *args, **kwargs) -> None:
    """Log an info message."""
    logger.info(msg, *args, **kwargs)

def warning(msg: str, *args, **kwargs) -> None:
    """Log a warning message."""
    logger.warning(msg, *args, **kwargs)

def error(msg: str, *args, **kwargs) -> None:
    """Log an error message."""
    logger.error(msg, *args, **kwargs)

def critical(msg: str, *args, **kwargs) -> None:
    """Log a critical message."""
    logger.critical(msg, *args, **kwargs)

def exception(msg: str, *args, **kwargs) -> None:
    """Log an exception message."""
    logger.exception(msg, *args, **kwargs)