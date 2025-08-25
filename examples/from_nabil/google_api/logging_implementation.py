"""
Comprehensive Logging Implementation

This module provides a centralized logging configuration for the application.
It configures different log levels, log rotation, and formatting.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Constants
LOG_DIR = "logs"
LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 7  # Keep logs for one week

# Ensure log directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def get_logger(name, log_file=None, level=logging.INFO):
    """
    Get a logger with the given name and configuration.
    
    Args:
        name (str): Name of the logger, typically the module name
        log_file (str, optional): File to log to. If None, uses {name}.log
        level (int, optional): Logging level. Defaults to INFO.
        
    Returns:
        logging.Logger: Configured logger instance
    """
    if log_file is None:
        log_file = f"{name}.log"
    
    # Create full path for log file
    log_path = os.path.join(LOG_DIR, log_file)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Check if handlers are already configured to avoid duplicates
    if not logger.handlers:
        # File handler with rotation
        file_handler = RotatingFileHandler(
            log_path, 
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT
        )
        file_handler.setLevel(level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        # Create formatter and add it to the handlers
        formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

# Set up root logger
root_logger = get_logger("app", "application.log")

# Create component-specific loggers
api_logger = get_logger("api", "api.log")
database_logger = get_logger("database", "database.log")
notifier_logger = get_logger("notifier", "notifier.log")

# Set debug level for development
def set_debug_mode():
    """Enable debug logging for all loggers"""
    root_logger.setLevel(logging.DEBUG)
    api_logger.setLevel(logging.DEBUG)
    database_logger.setLevel(logging.DEBUG)
    notifier_logger.setLevel(logging.DEBUG)

# Add context to logs
class LogContext:
    """Context manager for adding context to logs"""
    def __init__(self, logger, context):
        self.logger = logger
        self.original_format = LOG_FORMAT
        self.context = context
        
    def __enter__(self):
        for handler in self.logger.handlers:
            formatter = handler.formatter
            if formatter:
                context_format = LOG_FORMAT.replace(
                    "%(message)s", 
                    f"[{self.context}] %(message)s"
                )
                handler.setFormatter(
                    logging.Formatter(context_format, DATE_FORMAT)
                )
        return self.logger
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        for handler in self.logger.handlers:
            handler.setFormatter(
                logging.Formatter(self.original_format, DATE_FORMAT)
            )
