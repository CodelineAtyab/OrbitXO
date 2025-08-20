import logging
import logging.handlers
import os
import requests
import json
import datetime
import traceback
from pathlib import Path

class JSONLogFormatter(logging.Formatter):
    """
    Custom formatter that outputs logs in JSON format
    """
    def format(self, record):
        # Get the original formatted message
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "file": record.filename,
            "line": record.lineno,
            "message": record.getMessage()
        }
        
        # Add exception info if present
        if record.exc_info:
            log_record["traceback"] = traceback.format_exception(*record.exc_info)
        
        # Add context if available
        if hasattr(record, 'context'):
            log_record["context"] = record.context
            
        return json.dumps(log_record)

class LoggingSystem:
    """
    A comprehensive logging system that implements Python's built-in logging library
    with rotation, different log levels, and JSON formatting.
    """
    
    def __init__(self, app_name="OrbitXO", log_dir=None, use_json=True):
        """
        Initialize the logging system with the application name and log directory
        
        Args:
            app_name (str): Name of the application for logging purposes
            log_dir (str): Directory to store log files, defaults to logs directory in project root
            use_json (bool): Whether to output logs in JSON format
            log_dir (str): Directory to store log files, defaults to logs directory in project root
        """
        self.app_name = app_name
        self.use_json = use_json
        
        # Set up log directory path
        if log_dir is None:
            # Get the project root directory (3 levels up from this file)
            current_dir = Path(__file__).resolve().parent
            project_root = current_dir.parent.parent.parent
            self.log_dir = project_root / 'logs'
        else:
            self.log_dir = Path(log_dir)
            
        # Ensure log directory exists
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Set up the logger
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(logging.DEBUG)  # Capture all levels
        
        # Clear any existing handlers
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Create log formatters
        self.setup_formatters()
        
        # Set up handlers
        self.setup_file_handler()
        self.setup_console_handler()
        
        # Set up JSON log file
        if self.use_json:
            self.setup_json_log_file()
        
        # Log initialization
        self.log_with_context('info', "Logging system initialized", {"app_name": app_name})
    
    def setup_formatters(self):
        """Set up formatters for different handlers"""
        # Standard format for file logs: timestamp loglevel [filename] message
        self.file_formatter = logging.Formatter(
            '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # JSON formatter
        self.json_formatter = JSONLogFormatter(
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    def setup_file_handler(self):
        """Set up file handler with rotation"""
        log_file = self.log_dir / 'application.log'
        
        # Set up a rotating file handler (7 days of logs)
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=log_file,
            when='midnight',
            interval=1,
            backupCount=7  # Keep logs for one week
        )
        
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(self.file_formatter)
        self.logger.addHandler(file_handler)
        
        # Set up a separate file handler for DEBUG level and above
        debug_log_file = self.log_dir / 'debug.log'
        debug_file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=debug_log_file,
            when='midnight',
            interval=1,
            backupCount=3  # Keep debug logs for 3 days only
        )
        
        debug_file_handler.setLevel(logging.DEBUG)
        debug_file_handler.setFormatter(self.file_formatter)
        self.logger.addHandler(debug_file_handler)
        
        # Set up a separate file handler for errors
        error_log_file = self.log_dir / 'error.log'
        error_file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=error_log_file,
            when='midnight',
            interval=1,
            backupCount=7  # Keep error logs for a week
        )
        
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(self.file_formatter)
        self.logger.addHandler(error_file_handler)
    
    def setup_console_handler(self):
        """Set up console handler for development"""
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(self.file_formatter)
        self.logger.addHandler(console_handler)
        
    def setup_json_log_file(self):
        """Set up JSON log file handler"""
        # Create JSON log directory if it doesn't exist
        json_log_dir = Path(__file__).resolve().parent
        os.makedirs(json_log_dir, exist_ok=True)
        
        # Set up JSON log file
        json_log_file = json_log_dir / 'logging_output.json'
        
        # Create an empty JSON log file if it doesn't exist
        if not json_log_file.exists():
            with open(json_log_file, 'w') as f:
                json.dump({"loggers": []}, f, indent=2)
        
        # We don't add a handler for JSON logs because we'll write them manually
        # to maintain the array structure
    
    def log_with_context(self, level, message, context=None):
        """
        Log a message with added context
        
        Args:
            level (str): Log level (debug, info, warning, error, critical)
            message (str): The log message
            context (dict): Additional context to include in the log
        """
        if context is None:
            context = {}
            
        # Add context to the log record
        extra = {'context': context}
        
        # Format message for regular log files
        context_str = f" - Context: {json.dumps(context)}" if context else ""
        full_message = f"{message}{context_str}"
        
        # Log at the appropriate level
        if level.lower() == 'debug':
            self.logger.debug(full_message, extra=extra)
        elif level.lower() == 'info':
            self.logger.info(full_message, extra=extra)
        elif level.lower() == 'warning':
            self.logger.warning(full_message, extra=extra)
        elif level.lower() == 'error':
            self.logger.error(full_message, extra=extra)
        elif level.lower() == 'critical':
            self.logger.critical(full_message, extra=extra)
            
        # If JSON logging is enabled, also write to the JSON log file
        if self.use_json:
            self.write_to_json_log(level, message, context)
    
    def write_to_json_log(self, level, message, context=None):
        """
        Write a log entry to the JSON log file
        
        Args:
            level (str): Log level
            message (str): The log message
            context (dict): Additional context to include in the log
        """
        try:
            # Get the current frame info to determine file and line number
            frame = traceback._getframe(2)  # Get the caller's frame
            filename = os.path.basename(frame.f_code.co_filename)
            lineno = frame.f_lineno
            
            # Create log entry
            log_entry = {
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "level": level.upper(),
                "file": filename,
                "line": lineno,
                "message": message
            }
            
            # Add context if available
            if context:
                log_entry["context"] = context
                
            # Read existing logs
            json_log_file = Path(__file__).resolve().parent / 'logging_output.json'
            with open(json_log_file, 'r') as f:
                log_data = json.load(f)
                
            # Append new log entry
            log_data["loggers"].append(log_entry)
            
            # Write updated logs back to file
            with open(json_log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            # If there's an error writing to the JSON log, fall back to console
            print(f"Error writing to JSON log: {str(e)}")
    
    def log_api_request(self, api_name, endpoint, params=None, headers=None):
        """
        Log an API request
        
        Args:
            api_name (str): Name of the API being called
            endpoint (str): API endpoint
            params (dict): Request parameters
            headers (dict): Request headers (sensitive data will be redacted)
        """
        # Create a safe copy of headers with sensitive information redacted
        safe_headers = None
        if headers:
            safe_headers = headers.copy()
            for key in safe_headers:
                if 'auth' in key.lower() or 'key' in key.lower() or 'token' in key.lower():
                    safe_headers[key] = '****REDACTED****'
        
        context = {
            "api": api_name,
            "endpoint": endpoint,
            "request_params": params,
            "headers": safe_headers
        }
        
        self.log_with_context('info', f"Starting API request to {api_name}", context)
    
    def log_api_response(self, api_name, status_code, response_summary=None):
        """
        Log an API response
        
        Args:
            api_name (str): Name of the API that was called
            status_code (int): HTTP status code
            response_summary (dict): Summary of the response (avoid logging full responses)
        """
        context = {
            "api": api_name,
            "status_code": status_code,
            "response_summary": response_summary
        }
        
        if 200 <= status_code < 300:
            self.log_with_context('info', f"Received response: {status_code} OK", context)
        elif 400 <= status_code < 500:
            self.log_with_context('warning', f"API request error: {status_code}", context)
        elif status_code >= 500:
            self.log_with_context('error', f"API server error: {status_code}", context)
    
    def log_database_operation(self, operation, table, record_id=None, details=None):
        """
        Log a database operation
        
        Args:
            operation (str): Database operation (SELECT, INSERT, UPDATE, DELETE)
            table (str): Table being operated on
            record_id (int/str): ID of the record (if applicable)
            details (dict): Additional details about the operation
        """
        context = {
            "operation": operation,
            "table": table,
            "record_id": record_id,
            "details": details
        }
        
        self.log_with_context('info', f"Database {operation}: {table}", context)
    
    def log_application_event(self, event_type, details=None):
        """
        Log an application event
        
        Args:
            event_type (str): Type of event
            details (dict): Additional details about the event
        """
        if details is None:
            details = {}
            
        context = {
            "event_type": event_type,
            "details": details,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        self.log_with_context('info', f"Application event: {event_type}", context)


class GoogleMapsClient:
    """
    Client for making requests to Google Maps API and logging the interactions
    """
    
    def __init__(self, logger):
        """
        Initialize the Google Maps client
        
        Args:
            logger (LoggingSystem): The logging system to use
        """
        self.logger = logger
        self.base_url = "https://maps.googleapis.com/maps/api"
        # In a real app, you would get this from environment variables or a secure config
        self.api_key = "YOUR_API_KEY"  # Placeholder - replace with a real key in production
        
    def get_travel_time(self, source, destination):
        """
        Get travel time between two locations
        
        Args:
            source (str): Starting location
            destination (str): Ending location
            
        Returns:
            dict: Travel time information
        """
        endpoint = "/directions/json"
        params = {
            "origin": source,
            "destination": destination,
            "key": self.api_key
        }
        
        # Log the API request (redacting the API key)
        safe_params = params.copy()
        safe_params["key"] = "****REDACTED****"
        self.logger.log_api_request("Google Maps", endpoint, safe_params)
        
        try:
            # For demonstration, we'll simulate an API call instead of making a real one
            # In a real app, you would use: response = requests.get(f"{self.base_url}{endpoint}", params=params)
            # Instead, we'll simulate a successful response:
            
            # Simulated successful response
            travel_data = {
                "status": "OK",
                "routes": [
                    {
                        "legs": [
                            {
                                "duration": {
                                    "text": "25 minutes",
                                    "value": 1500  # seconds
                                },
                                "distance": {
                                    "text": "15.2 km",
                                    "value": 15200  # meters
                                }
                            }
                        ]
                    }
                ]
            }
            
            # Log the API response
            self.logger.log_api_response("Google Maps", 200, {"status": "OK"})
            
            # Extract and return travel time data
            duration_text = travel_data["routes"][0]["legs"][0]["duration"]["text"]
            duration_seconds = travel_data["routes"][0]["legs"][0]["duration"]["value"]
            
            return {
                "duration_text": duration_text,
                "duration_seconds": duration_seconds,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            # Log any errors
            self.logger.log_with_context('error', f"Error fetching travel time", {
                "error": str(e),
                "source": source,
                "destination": destination
            })
            raise


class TravelTimeTracker:
    """
    Class for tracking and storing travel times between locations
    """
    
    def __init__(self, logger, data_file=None):
        """
        Initialize the travel time tracker
        
        Args:
            logger (LoggingSystem): The logging system to use
            data_file (str): Path to the JSON file for storing travel times
        """
        self.logger = logger
        
        # Set up data file path
        if data_file is None:
            # Get the project root directory
            current_dir = Path(__file__).resolve().parent
            project_root = current_dir.parent.parent
            self.data_file = project_root / 'travel_times.json'
        else:
            self.data_file = Path(data_file)
        
        # Load existing data or create new data structure
        self.load_data()
        
    def load_data(self):
        """Load travel time data from JSON file"""
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r') as file:
                    self.data = json.load(file)
                self.logger.log_with_context('debug', "Travel times data loaded", {
                    "file": str(self.data_file),
                    "routes": len(self.data)
                })
            else:
                self.data = {}
                self.logger.log_with_context('info', "No existing travel times data, creating new data structure")
        except Exception as e:
            self.logger.log_with_context('error', "Error loading travel times data", {"error": str(e)})
            self.data = {}
    
    def save_data(self):
        """Save travel time data to JSON file"""
        try:
            with open(self.data_file, 'w') as file:
                json.dump(self.data, file, indent=2)
            self.logger.log_with_context('debug', "Travel times data saved", {
                "file": str(self.data_file),
                "routes": len(self.data)
            })
        except Exception as e:
            self.logger.log_with_context('error', "Error saving travel times data", {"error": str(e)})
    
    def update_travel_time(self, route_key, source, destination, travel_time):
        """
        Update travel time for a route
        
        Args:
            route_key (str): Unique identifier for the route
            source (str): Starting location
            destination (str): Ending location
            travel_time (dict): Travel time information from Google Maps API
        """
        # Log the database operation
        self.logger.log_database_operation("INSERT", "travel_times", route_key, {
            "travel_time": travel_time["duration_text"],
            "route": f"{source} to {destination}"
        })
        
        # Create or update route data
        if route_key not in self.data:
            self.data[route_key] = {
                "source": source,
                "destination": destination,
                "min_duration": travel_time["duration_seconds"],
                "recorded_at": travel_time["timestamp"],
                "history": []
            }
            
        # Add to history
        self.data[route_key]["history"].append({
            "duration": travel_time["duration_seconds"],
            "timestamp": travel_time["timestamp"]
        })
        
        # Update min duration if new time is faster
        if travel_time["duration_seconds"] < self.data[route_key]["min_duration"]:
            self.data[route_key]["min_duration"] = travel_time["duration_seconds"]
            self.data[route_key]["recorded_at"] = travel_time["timestamp"]
            
            # Log this as a notable event
            self.logger.log_application_event("new_minimum_travel_time", {
                "route": f"{source} to {destination}",
                "new_minimum": travel_time["duration_text"],
                "previous_records": len(self.data[route_key]["history"])
            })
        
        # Save data to file
        self.save_data()


def main():
    """Main function to demonstrate the logging system"""
    
    # Initialize the logging system
    logging_system = LoggingSystem(app_name="OrbitXO")
    logger = logging_system
    
    # Log application start
    logger.log_with_context('info', "Application started")
    
    # Log configuration loading
    logger.log_with_context('debug', "Configuration loaded", {"config_file": "settings.json"})
    
    try:
        # Initialize Google Maps client
        maps_client = GoogleMapsClient(logger)
        
        # Initialize travel time tracker
        tracker = TravelTimeTracker(logger)
        
        # Get travel time from home to work
        travel_time = maps_client.get_travel_time("home", "work")
        
        # Update travel time
        tracker.update_travel_time("home_work", "Home", "Work", travel_time)
        
        # Log a successful notification
        logger.log_application_event("notification_sent", {
            "channel": "Slack",
            "recipient": "team",
            "message": "Daily travel time updated"
        })
        
        # Log a warning
        logger.log_with_context('warning', "Slack notification delivery delayed", {"retry_count": 1})
        
        # Demonstrate error logging
        try:
            # This will cause a division by zero error
            result = 10 / 0
        except Exception as e:
            logger.log_with_context('error', f"Failed to calculate result", {"operation": "division"})
            logger.logger.exception(e)  # This logs the full traceback
    
    except Exception as e:
        # Log any unexpected errors
        logger.log_with_context('critical', "Unhandled exception in main function", {"error": str(e)})
        logger.logger.exception(e)  # This logs the full traceback


if __name__ == "__main__":
    main()
