import os
import logging
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
LOG_DIR = "logs"
LOG_LEVEL = logging.INFO

# Create logs directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

# Set up simple loggers
def setup_logger(name, filename):
    """
    Set up a logger with file handler.
    
    Args:
        name (str): Logger name
        filename (str): Log filename
        
    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # Remove any existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Create file handler
    file_handler = logging.FileHandler(os.path.join(LOG_DIR, filename), encoding='utf-8')
    file_handler.setLevel(LOG_LEVEL)
    
    # Create simple formatter
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # Add handler
    logger.addHandler(file_handler)
    
    return logger

# Create individual loggers
api_logger = setup_logger("api_calls", "api.log")
route_logger = setup_logger("route_tracker", "route.log")
slack_logger = setup_logger("slack_notifications", "notifier.log")
error_logger = setup_logger("errors", "error.log")
application_logger = setup_logger("application", "application.log")
    
# Simple logging functions

def log_api_call(origin, destination, mode, api_key_used=None, response_status=None, response_data=None):
    """
    Log a call to the Google Maps API.
    
    Args:
        origin: Origin location
        destination: Destination location
        mode: Transportation mode
        api_key_used: Whether an API key was provided (True/False)
        response_status: Response status code
        response_data: JSON response data (optional)
    """
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "origin": origin,
        "destination": destination,
        "mode": mode,
        "api_key_provided": api_key_used is not None,
        "response_status": response_status
    }
    
    # Include summary of response data if available
    if response_data and isinstance(response_data, dict):
        status = response_data.get("status")
        log_data["api_status"] = status
        
        # Add error message if available
        if status != "OK" and "error_message" in response_data:
            log_data["error_message"] = response_data["error_message"]
    
    message = json.dumps(log_data)
    api_logger.info(message)
    
    # Log errors separately
    if response_status != 200 or (response_data and response_data.get("status") != "OK"):
        error_logger.warning(f"API call failed: {message}")

def log_route_tracking(route_data, continuous_tracking=False, check_interval=None):
    """
    Log route tracking information.
    
    Args:
        route_data: Dictionary containing route information
        continuous_tracking: Whether continuous tracking is enabled
        check_interval: Interval between checks (if continuous tracking)
    """
    if not route_data:
        route_logger.warning("Route tracking failed: No route data available")
        return
    
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "tracking_time": route_data.get("timestamp"),
        "origin": route_data.get("origin"),
        "destination": route_data.get("destination"),
        "distance": route_data.get("distance_text"),
        "duration": route_data.get("duration_text"),
        "is_min_distance": route_data.get("is_min_distance", False),
        "is_min_duration": route_data.get("is_min_duration", False)
    }
    
    if continuous_tracking:
        log_data["continuous_tracking"] = True
        if check_interval:
            log_data["check_interval_seconds"] = check_interval
    
    route_logger.info(json.dumps(log_data))

def log_slack_notification(route_data, success=True, error_message=None):
    """
    Log Slack notification information.
    
    Args:
        route_data: Dictionary containing route information
        success: Whether the notification was sent successfully
        error_message: Error message if notification failed
    """
    if not route_data:
        slack_logger.warning("Slack notification attempted without route data")
        return
        
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "origin": route_data.get("origin"),
        "destination": route_data.get("destination"),
        "success": success
    }
    
    if not success and error_message:
        log_data["error_message"] = error_message
        error_logger.error(f"Slack notification failed: {error_message}")
    
    slack_logger.info(json.dumps(log_data))

def log_error(module, function, error_message):
    """
    Log general errors.
    
    Args:
        module: Module name
        function: Function name
        error_message: Error message
    """
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "module": module,
        "function": function,
        "error": error_message
    }
    
    error_logger.error(json.dumps(log_data))
    
def log_app_info(message, **extra_data):
    """
    Log general application information.
    
    Args:
        message: Log message
        extra_data: Additional data to include in the log
    """
    if extra_data:
        message = f"{message} - {json.dumps(extra_data)}"
    
    application_logger.info(message)

if __name__ == "__main__":
    """
    Simple examples of using the logger functions
    """
    print("Simple API Logger Example")
    print("========================")
    
    # Example 1: Log API call with success
    print("Example 1: Logging successful API call...")
    log_api_call(
        origin="Seattle, WA",
        destination="Portland, OR",
        mode="DRIVE",
        api_key_used=True,
        response_status=200,
        response_data={"status": "OK"}
    )
    
    # Example 2: Log API call with error
    print("Example 2: Logging failed API call...")
    log_api_call(
        origin="Invalid Location",
        destination="Portland, OR",
        mode="DRIVE",
        api_key_used=True,
        response_status=400,
        response_data={"status": "INVALID_REQUEST", "error_message": "Invalid origin"}
    )
    
    # Example 3: Log route tracking
    print("Example 3: Logging route tracking...")
    test_route_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "origin": "Seattle, WA",
        "destination": "Portland, OR",
        "distance_meters": 280000,
        "distance_text": "280 km",
        "duration_seconds": 10800,
        "duration_text": "3 hours",
        "is_min_distance": True,
        "is_min_duration": True
    }
    log_route_tracking(test_route_data)
    
    # Example 4: Log Slack notification
    print("Example 4: Logging Slack notification...")
    log_slack_notification(test_route_data, success=True)
    
    # Example 5: Log application info
    print("Example 5: Logging general application info...")
    log_app_info("Application started", version="1.0.0", user="test_user")
    
    # Example 6: Log error
    print("Example 6: Logging error...")
    log_error("api_module", "get_distance", "Connection timed out")
    
    print("\nLog files created in 'logs' directory:")
    print("- api.log: API calls")
    print("- route.log: Route tracking")
    print("- notifier.log: Slack notifications")
    print("- error.log: Error messages")
    print("- application.log: General application logs")
