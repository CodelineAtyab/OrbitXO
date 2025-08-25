"""
Advanced Logging System

This module provides a comprehensive logging system with features like:
- Multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Log rotation with configurable retention
- Different formatters for console and file output
- Specialized loggers for different components (API, database, etc.)
- Structured JSON logging for machine parsing
"""

import os
import sys
import json
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get log level from environment or use INFO as default
DEFAULT_LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
LOG_LEVEL_MAP = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

class AdvancedLogger:
    """
    Advanced logging system with log rotation, multiple log levels,
    and consistent formatting.
    """
    
    def __init__(self, log_dir="logs", log_level=None, console_output=True):
        """
        Initialize the advanced logger.
        
        Args:
            log_dir (str): Directory to store log files
            log_level (str): Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            console_output (bool): Whether to also output logs to console
        """
        self.log_dir = log_dir
        
        # Set log level from parameter, environment, or default
        if log_level is None:
            self.log_level = LOG_LEVEL_MAP.get(DEFAULT_LOG_LEVEL, logging.INFO)
        else:
            self.log_level = LOG_LEVEL_MAP.get(log_level.upper(), logging.INFO)
        
        self.console_output = console_output
        
        # Create logs directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Set up loggers for different components
        self.api_logger = self._setup_logger("api", "api.log")
        self.database_logger = self._setup_logger("database", "database.log")
        self.route_logger = self._setup_logger("route", "route.log")
        self.notifier_logger = self._setup_logger("notifier", "notifier.log")
        self.error_logger = self._setup_logger("error", "error.log")
        
        # Application-wide logger
        self.app_logger = self._setup_logger("application", "application.log")
        
        # Dictionary to store logger instances
        self.loggers = {
            "api": self.api_logger,
            "database": self.database_logger,
            "route": self.route_logger,
            "notifier": self.notifier_logger,
            "error": self.error_logger,
            "application": self.app_logger
        }
    
    def _setup_logger(self, name, filename):
        """
        Set up a logger with file and console handlers and log rotation.
        
        Args:
            name (str): Logger name
            filename (str): Log filename
            
        Returns:
            logging.Logger: Configured logger
        """
        logger = logging.getLogger(name)
        logger.setLevel(self.log_level)
        logger.propagate = False  # Don't propagate to parent loggers
        
        # Remove any existing handlers
        if logger.hasHandlers():
            logger.handlers.clear()
        
        # Create rotating file handler (rotate at midnight, keep for 7 days)
        file_path = os.path.join(self.log_dir, filename)
        file_handler = TimedRotatingFileHandler(
            file_path, 
            when='midnight',
            interval=1,
            backupCount=7,  # Keep logs for one week
            encoding='utf-8'
        )
        file_handler.setLevel(self.log_level)
        
        # Create formatters
        file_formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s.py] %(message)s')
        file_handler.setFormatter(file_formatter)
        
        # Add file handler
        logger.addHandler(file_handler)
        
        # Add console handler if enabled
        if self.console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(self.log_level)
            
            # Use colored output for console if possible
            try:
                import colorlog
                color_formatter = colorlog.ColoredFormatter(
                    '%(log_color)s%(asctime)s %(levelname)s [%(name)s.py] %(message)s',
                    log_colors={
                        'DEBUG': 'cyan',
                        'INFO': 'green',
                        'WARNING': 'yellow',
                        'ERROR': 'red',
                        'CRITICAL': 'red,bg_white',
                    }
                )
                console_handler.setFormatter(color_formatter)
            except ImportError:
                console_formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s.py] %(message)s')
                console_handler.setFormatter(console_formatter)
            
            logger.addHandler(console_handler)
        
        return logger
    
    def _format_object(self, obj):
        """Format an object for logging, handling various types."""
        if isinstance(obj, dict):
            return json.dumps(obj)
        return str(obj)
    
    def get_logger(self, component):
        """
        Get a logger for a specific component.
        
        Args:
            component (str): Component name (api, database, route, notifier, error, application)
            
        Returns:
            logging.Logger: Logger instance
        """
        return self.loggers.get(component, self.app_logger)
    
    def log(self, level, component, message, **kwargs):
        """
        Generic logging method.
        
        Args:
            level (str): Log level (debug, info, warning, error, critical)
            component (str): Component name
            message (str): Log message
            **kwargs: Additional data to include in the log
        """
        logger = self.get_logger(component)
        
        # Format additional data as JSON if present
        if kwargs:
            data_str = " " + json.dumps(kwargs)
        else:
            data_str = ""
            
        log_method = getattr(logger, level.lower(), logger.info)
        log_method(f"{message}{data_str}")
    
    # Convenience methods for different log levels
    def debug(self, component, message, **kwargs):
        """Log a debug message."""
        self.log("debug", component, message, **kwargs)
    
    def info(self, component, message, **kwargs):
        """Log an info message."""
        self.log("info", component, message, **kwargs)
    
    def warning(self, component, message, **kwargs):
        """Log a warning message."""
        self.log("warning", component, message, **kwargs)
    
    def error(self, component, message, **kwargs):
        """Log an error message."""
        self.log("error", component, message, **kwargs)
        # Also log to error logger
        if component != "error":
            self.error_logger.error(f"[{component}] {message} {self._format_object(kwargs) if kwargs else ''}")
    
    def critical(self, component, message, **kwargs):
        """Log a critical message."""
        self.log("critical", component, message, **kwargs)
        # Also log to error logger
        if component != "error":
            self.error_logger.critical(f"[{component}] {message} {self._format_object(kwargs) if kwargs else ''}")
    
    # API-specific logging methods
    def log_api_request(self, endpoint, params=None, headers=None):
        """
        Log an API request.
        
        Args:
            endpoint (str): API endpoint
            params (dict): Request parameters
            headers (dict): Request headers
        """
        self.debug("api", f"Starting API request to {endpoint}", 
                 params=params, 
                 headers={k: v for k, v in (headers or {}).items() if k.lower() != 'authorization'})
    
    def log_api_response(self, endpoint, status_code, response_data=None):
        """
        Log an API response.
        
        Args:
            endpoint (str): API endpoint
            status_code (int): Response status code
            response_data (dict): Response data
        """
        if 200 <= status_code < 300:
            self.info("api", f"Received response from {endpoint}", 
                     status_code=status_code, 
                     data=response_data)
        else:
            self.warning("api", f"Received error response from {endpoint}", 
                        status_code=status_code, 
                        error=response_data)
    
    def log_api_error(self, endpoint, error_message):
        """
        Log an API error.
        
        Args:
            endpoint (str): API endpoint
            error_message (str): Error message
        """
        self.error("api", f"Error calling {endpoint}", error=error_message)
    
    # Database-specific logging methods
    def log_db_operation(self, operation, table, data=None, query=None):
        """
        Log a database operation.
        
        Args:
            operation (str): Operation type (SELECT, INSERT, UPDATE, DELETE)
            table (str): Table name
            data (dict): Data being inserted/updated
            query (str): SQL query
        """
        self.info("database", f"{operation} on {table}", data=data, query=query)
    
    def log_db_error(self, operation, table, error_message):
        """
        Log a database error.
        
        Args:
            operation (str): Operation type
            table (str): Table name
            error_message (str): Error message
        """
        self.error("database", f"Error during {operation} on {table}", error=error_message)
    
    # Route tracking logging methods
    def log_route_check(self, origin, destination, result=None):
        """
        Log a route check.
        
        Args:
            origin (str): Origin location
            destination (str): Destination location
            result (dict): Route result data
        """
        self.info("route", f"Checked route from {origin} to {destination}", result=result)
    
    def log_route_min(self, origin, destination, min_type, value, units):
        """
        Log a new minimum route.
        
        Args:
            origin (str): Origin location
            destination (str): Destination location
            min_type (str): Type of minimum (distance, duration)
            value: Minimum value
            units (str): Units (meters, seconds)
        """
        self.info("route", f"New minimum {min_type} from {origin} to {destination}", 
                value=value, units=units)
    
    # Notification logging methods
    def log_notification_attempt(self, channel, message_type):
        """
        Log a notification attempt.
        
        Args:
            channel (str): Notification channel (e.g., Slack, Email)
            message_type (str): Type of message being sent
        """
        self.info("notifier", f"Attempting to send {message_type} notification via {channel}")
    
    def log_notification_success(self, channel, message_id=None):
        """
        Log a successful notification.
        
        Args:
            channel (str): Notification channel
            message_id (str): Message ID if available
        """
        self.info("notifier", f"Successfully sent notification via {channel}", message_id=message_id)
    
    def log_notification_failure(self, channel, error_message, retry=False):
        """
        Log a notification failure.
        
        Args:
            channel (str): Notification channel
            error_message (str): Error message
            retry (bool): Whether a retry will be attempted
        """
        level = "warning" if retry else "error"
        message = f"Failed to send notification via {channel}"
        if retry:
            message += ", retrying..."
        
        getattr(self, level)("notifier", message, error=error_message)

# Create a singleton instance
advanced_logger = AdvancedLogger()

# Convenience functions
def debug(component, message, **kwargs):
    return advanced_logger.debug(component, message, **kwargs)

def info(component, message, **kwargs):
    return advanced_logger.info(component, message, **kwargs)

def warning(component, message, **kwargs):
    return advanced_logger.warning(component, message, **kwargs)

def error(component, message, **kwargs):
    return advanced_logger.error(component, message, **kwargs)

def critical(component, message, **kwargs):
    return advanced_logger.critical(component, message, **kwargs)

# Specialized logging functions
def log_api_request(endpoint, params=None, headers=None):
    return advanced_logger.log_api_request(endpoint, params, headers)

def log_api_response(endpoint, status_code, response_data=None):
    return advanced_logger.log_api_response(endpoint, status_code, response_data)

def log_api_error(endpoint, error_message):
    return advanced_logger.error("api", f"Error calling {endpoint}", error=error_message)

def log_db_operation(operation, table, data=None, query=None):
    return advanced_logger.log_db_operation(operation, table, data, query)

def log_db_error(operation, table, error_message):
    return advanced_logger.error("database", f"Error during {operation} on {table}", error=error_message)

def log_route_check(origin, destination, result=None):
    return advanced_logger.log_route_check(origin, destination, result)

def log_route_min(origin, destination, min_type, value, units):
    return advanced_logger.info("route", f"New minimum {min_type} from {origin} to {destination}", 
                                value=value, units=units)

def log_notification_attempt(channel, message_type):
    return advanced_logger.log_notification_attempt(channel, message_type)

def log_notification_success(channel, message_id=None):
    return advanced_logger.log_notification_success(channel, message_id)

def log_notification_failure(channel, error_message, retry=False):
    return advanced_logger.log_notification_failure(channel, error_message, retry)

if __name__ == "__main__":
    # Test the logger with example logs matching the provided format
    print("Testing Advanced Logger...")
    
    # Example logs similar to the acceptance criteria
    info("api", "Starting API request to Google Maps")
    debug("api", "Request parameters", source="home", destination="work")
    info("api", "Received response: 200 OK")
    info("database", "Connecting to database")
    info("database", "Storing new travel time record: 26 minutes")
    warning("notifier", "Failed to send Slack notification, retrying...")
    info("notifier", "Slack notification sent successfully")
    
    # Additional test logs
    log_api_request("Google Maps Routes API", {"origin": "Seattle", "destination": "Portland"})
    log_api_response("Google Maps Routes API", 200, {"status": "OK"})
    log_db_operation("INSERT", "route_history", {"origin": "Seattle", "destination": "Portland"})
    log_route_check("Seattle", "Portland", {"distance": "280 km", "duration": "3 hours"})
    log_notification_attempt("Slack", "Route update")
    log_notification_success("Slack")
    log_notification_failure("Email", "Connection error", retry=True)
    
    print("Log entries created successfully in the 'logs' directory.")
    print("Log files will be rotated daily and kept for 7 days.")
