import os
import logging
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ApiLogger:
    """
    A logger class to track calls to the Google Maps API, route tracker, and Slack notifications.
    """
    
    def __init__(self, log_dir="logs", log_level=logging.INFO):
        """
        Initialize the logger.
        
        Args:
            log_dir (str): Directory to store log files
            log_level: Logging level (default: INFO)
        """
        self.log_dir = log_dir
        self.log_level = log_level
        
        # Create logs directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Set up loggers
        self.api_logger = self._setup_logger("api_calls", "api_calls.log")
        self.route_logger = self._setup_logger("route_tracker", "route_tracking.log")
        self.slack_logger = self._setup_logger("slack_notifications", "slack_notifications.log")
        self.error_logger = self._setup_logger("errors", "errors.log")
    
    def _setup_logger(self, name, filename):
        """
        Set up a logger with file and console handlers.
        
        Args:
            name (str): Logger name
            filename (str): Log filename
            
        Returns:
            logging.Logger: Configured logger
        """
        logger = logging.getLogger(name)
        logger.setLevel(self.log_level)
        
        # Remove any existing handlers
        if logger.hasHandlers():
            logger.handlers.clear()
        
        # Create file handler
        file_handler = logging.FileHandler(os.path.join(self.log_dir, filename), encoding='utf-8')
        file_handler.setLevel(self.log_level)
        
        # Create formatters
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        
        # Add handlers
        logger.addHandler(file_handler)
        
        return logger
    
    def log_api_call(self, origin, destination, mode, api_key_used=None, response_status=None, response_data=None):
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
            "service": "Google Maps Routes API",
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
        
        self.api_logger.info(json.dumps(log_data))
        
        # Log errors separately
        if response_status != 200 or (response_data and response_data.get("status") != "OK"):
            self.error_logger.warning(f"API call failed: {json.dumps(log_data)}")
    
    def log_route_tracking(self, route_data, continuous_tracking=False, check_interval=None):
        """
        Log route tracking information.
        
        Args:
            route_data: Dictionary containing route information
            continuous_tracking: Whether continuous tracking is enabled
            check_interval: Interval between checks (if continuous tracking)
        """
        if not route_data:
            self.route_logger.warning("Route tracking failed: No route data available")
            return
        
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "tracking_time": route_data.get("timestamp"),
            "origin": route_data.get("origin"),
            "destination": route_data.get("destination"),
            "distance_meters": route_data.get("distance_meters"),
            "distance_text": route_data.get("distance_text"),
            "duration_seconds": route_data.get("duration_seconds"),
            "duration_text": route_data.get("duration_text"),
            "is_min_distance": route_data.get("is_min_distance", False),
            "is_min_duration": route_data.get("is_min_duration", False),
            "continuous_tracking": continuous_tracking
        }
        
        if continuous_tracking and check_interval:
            log_data["check_interval_seconds"] = check_interval
        
        self.route_logger.info(json.dumps(log_data))
    
    def log_slack_notification(self, route_data, success=True, error_message=None):
        """
        Log Slack notification information.
        
        Args:
            route_data: Dictionary containing route information
            success: Whether the notification was sent successfully
            error_message: Error message if notification failed
        """
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "notification_time": route_data.get("timestamp") if route_data else None,
            "success": success
        }
        
        if route_data:
            log_data.update({
                "origin": route_data.get("origin"),
                "destination": route_data.get("destination"),
                "distance": route_data.get("distance_text"),
                "duration": route_data.get("duration_text")
            })
        
        if not success and error_message:
            log_data["error_message"] = error_message
            self.error_logger.error(f"Slack notification failed: {error_message}")
        
        self.slack_logger.info(json.dumps(log_data))
    
    def log_error(self, module, function, error_message):
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
        
        self.error_logger.error(json.dumps(log_data))

# Create a singleton instance
logger = ApiLogger()

# Convenience functions
def log_api_call(*args, **kwargs):
    return logger.log_api_call(*args, **kwargs)

def log_route_tracking(*args, **kwargs):
    return logger.log_route_tracking(*args, **kwargs)

def log_slack_notification(*args, **kwargs):
    return logger.log_slack_notification(*args, **kwargs)

def log_error(*args, **kwargs):
    return logger.log_error(*args, **kwargs)

if __name__ == "__main__":
    # Test the logger
    print("Testing API Logger...")
    
    # Test API call logging
    log_api_call(
        "Seattle, WA",
        "Portland, OR",
        "DRIVE",
        api_key_used=True,
        response_status=200,
        response_data={"status": "OK"}
    )
    
    # Test route tracking logging
    test_route_data = {
        "timestamp": datetime.now().isoformat(),
        "origin": "Seattle, WA",
        "destination": "Portland, OR",
        "distance_meters": 280000,
        "distance_text": "280 km",
        "duration_seconds": 10800,
        "duration_text": "3 hours",
        "is_min_distance": True,
        "is_min_duration": True
    }
    
    log_route_tracking(test_route_data, continuous_tracking=True, check_interval=300)
    
    # Test Slack notification logging
    log_slack_notification(test_route_data, success=True)
    
    # Test error logging
    log_error("test_module", "test_function", "This is a test error message")
    
    print("Log entries created successfully in the 'logs' directory.")
