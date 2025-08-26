import logging
import logging.handlers
import os
import sys
from datetime import datetime
import json
import inspect
import time

class LoggingConfig:
    
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    
    DEFAULT_LOG_DIR = "logs"
    
    def __init__(self, app_name="application", log_dir=None, log_level=logging.INFO,
                 max_bytes=10*1024*1024, backup_count=7, console_output=True):
        self.app_name = app_name
        self.log_dir = log_dir or self.DEFAULT_LOG_DIR
        self.log_level = log_level
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        self.console_output = console_output
        
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        self.configure_root_logger()
        
        self.loggers = {}
    
    def configure_root_logger(self):
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        root_logger.setLevel(self.log_level)
    
    def get_log_formatter(self, detailed=True):
        if detailed:
            return logging.Formatter('%(asctime)s %(levelname)s [%(module)s] %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S')
        else:
            return logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    def get_component_logger(self, component_name):
        if component_name in self.loggers:
            return self.loggers[component_name]
        
        logger = logging.getLogger(component_name)
        logger.setLevel(self.log_level)
        logger.propagate = False
        
        file_path = os.path.join(self.log_dir, f"{self.app_name}_{component_name}.log")
        file_handler = logging.handlers.RotatingFileHandler(
            file_path, maxBytes=self.max_bytes, backupCount=self.backup_count)
        file_handler.setFormatter(self.get_log_formatter())
        logger.addHandler(file_handler)
        
        if self.console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(self.get_log_formatter())
            logger.addHandler(console_handler)
        
        self.loggers[component_name] = logger
        
        return logger
    
    def get_default_logger(self):
        return self.get_component_logger("main")

class LogExecutionTime:
    
    def __init__(self, logger, operation_name):
        self.logger = logger
        self.operation_name = operation_name
    
    def __enter__(self):
        self.start_time = time.time()
        self.logger.info(f"Starting {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        execution_time = end_time - self.start_time
        
        if exc_type is not None:
            self.logger.error(f"{self.operation_name} failed after {execution_time:.2f} seconds: {exc_val}")
        else:
            self.logger.info(f"Completed {self.operation_name} in {execution_time:.2f} seconds")

def log_function_call(logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            frame = inspect.stack()[1]
            module = inspect.getmodule(frame[0])
            module_name = module.__name__ if module else "unknown"
            
            args_str = ", ".join([str(arg) for arg in args])
            kwargs_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
            params = f"{args_str}{', ' if args_str and kwargs_str else ''}{kwargs_str}"
            
            logger.debug(f"Calling {module_name}.{func_name}({params})")
            
            try:
                result = func(*args, **kwargs)
                
                result_str = str(result)
                if len(result_str) > 1000:
                    result_str = result_str[:1000] + "... [truncated]"
                logger.debug(f"{module_name}.{func_name} returned: {result_str}")
                
                return result
            except Exception as e:
                logger.error(f"{module_name}.{func_name} raised: {type(e).__name__}: {str(e)}")
                raise
        
        return wrapper
    
    return decorator

class ApiModule:
    
    def __init__(self, logging_config):
        self.logger = logging_config.get_component_logger("api")
    
    @log_function_call(logging.getLogger("api"))
    def make_api_request(self, url, params):
        self.logger.info(f"Starting API request to {url}")
        self.logger.debug(f"Request parameters: {json.dumps(params)}")
        
        time.sleep(1)
        
        response = {"status": 200, "data": {"result": "success"}}
        
        self.logger.info(f"Received response: {response['status']} OK")
        
        return response

class DatabaseModule:
    
    def __init__(self, logging_config):
        self.logger = logging_config.get_component_logger("database")
    
    def connect(self):
        self.logger.info("Connecting to database")
        time.sleep(0.5)
        self.logger.info("Connected to database successfully")
    
    def store_record(self, record_type, data):
        self.logger.info(f"Storing new {record_type} record")
        self.logger.debug(f"Record data: {json.dumps(data)}")
        
        time.sleep(0.5)
        
        self.logger.info(f"Successfully stored {record_type} record")
        
        if time.time() % 10 < 3:
            self.logger.warning("Database connection slow, consider optimization")

class NotifierModule:
    
    def __init__(self, logging_config):
        self.logger = logging_config.get_component_logger("notifier")
    
    def send_notification(self, channel, message):
        self.logger.info(f"Sending {channel} notification")
        
        time.sleep(0.5)
        
        if time.time() % 10 < 2:
            self.logger.warning(f"Failed to send {channel} notification, retrying...")
            time.sleep(0.5)
            
            if time.time() % 10 < 1:
                self.logger.error(f"Failed to send {channel} notification after retry")
                return False
            
            self.logger.info(f"{channel} notification sent successfully on retry")
            return True
        
        self.logger.info(f"{channel} notification sent successfully")
        return True

def run_demo():
    logging_config = LoggingConfig(
        app_name="travel_app",
        log_level=logging.DEBUG,
        backup_count=7,
        console_output=True
    )
    
    main_logger = logging_config.get_default_logger()
    main_logger.info("Application starting")
    
    try:
        api = ApiModule(logging_config)
        db = DatabaseModule(logging_config)
        notifier = NotifierModule(logging_config)
        
        with LogExecutionTime(main_logger, "complete travel time request workflow"):
            response = api.make_api_request("https://maps.googleapis.com/maps/api/directions/json", 
                                          {"source": "home", "destination": "work"})
            
            db.connect()
            
            travel_data = {
                "source": "home",
                "destination": "work",
                "duration_minutes": 26,
                "timestamp": datetime.now().isoformat()
            }
            db.store_record("travel_time", travel_data)
            
            notifier.send_notification("slack", "New travel time record created")
        
        main_logger.info("Application completed successfully")
    
    except Exception as e:
        main_logger.critical(f"Application failed with error: {str(e)}", exc_info=True)
    
if __name__ == "__main__":
    run_demo()
