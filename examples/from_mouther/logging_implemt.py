import logging
import os
import sys
import json
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

def setup_logger(name, log_level=logging.INFO, log_file=None):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    logger.handlers = []

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = TimedRotatingFileHandler(
            log_file,
            when='midnight', 
            interval=1,
            backupCount=7
        )
        file_handler.setLevel(log_level)

        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s'
        )
        file_handler.setFormatter(file_formatter)

        logger.addHandler(file_handler)

    return logger

def get_default_log_file(name):
    today = datetime.now().strftime('%Y-%m-%d')
    logs_dir = "logs"

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    return os.path.join(logs_dir, f"{name}.log")

def get_logger(name, log_level=logging.INFO, use_file=True):
    env_log_level = os.environ.get("LOG_LEVEL", "").upper()
    if env_log_level in LOG_LEVELS:
        log_level = LOG_LEVELS[env_log_level]

    log_file = get_default_log_file(name) if use_file else None
    return setup_logger(name, log_level, log_file)

def log_dict(logger, message, data, level=logging.INFO):
    try:
        json_str = json.dumps(data, indent=2)
        logger.log(level, f"{message}:\n{json_str}")
    except (TypeError, ValueError) as e:
        logger.error(f"Failed to log data as JSON: {e}")

def get_api_logger(api_name="api"):
    logger = get_logger(f"api.{api_name}")
    return logger

def get_db_logger(db_name="database"):
    logger = get_logger(f"db.{db_name}")
    return logger

def get_app_logger(component="app"):
    logger = get_logger(f"app.{component}")
    return logger

def log_api_call(logger, method, url, params=None, headers=None, response=None, error=None):
    log_data = {
        "method": method,
        "url": url,
        "params": params,

        "headers": {k: v for k, v in (headers or {}).items() if k.lower() not in ("authorization", "api-key", "x-goog-api-key")}

    }

    if response:
        log_data["status_code"] = getattr(response, "status_code", None)
        log_data["response_time"] = getattr(response, "elapsed", None)

    if error:
        logger.error(f"API call failed: {error}")
        log_dict(logger, "API call details", log_data, level=logging.ERROR)
    else:
        logger.info(f"API call to {url}")
        log_dict(logger, "API call details", log_data, level=logging.DEBUG)

=======
        
def log_google_maps_api_call(logger, source, destination, duration=None, distance=None, error=None):
    """
    Special logger method for Google Maps API calls
    """
    log_data = {
        "source": source,
        "destination": destination,
        "api": "Google Maps Directions API v2"
    }
    
    if duration is not None:
        log_data["duration_minutes"] = duration
        
    if distance is not None:
        log_data["distance_meters"] = distance
        
    if error:
        logger.error(f"Google Maps API call failed: {error}")
        log_dict(logger, "Google Maps API call details", log_data, level=logging.ERROR)
    else:
        logger.info(f"Google Maps API call: {source} → {destination}")
        log_dict(logger, "Google Maps API call details", log_data, level=logging.DEBUG)


def log_db_operation(logger, operation, table=None, query=None, params=None, result=None, error=None):
    log_data = {
        "operation": operation,
        "table": table,
        "query": query,
        "params": params
    }

    if result is not None:
        log_data["result_count"] = len(result) if hasattr(result, "__len__") else 1

    if error:
        logger.error(f"Database operation failed: {error}")
        log_dict(logger, "Database operation details", log_data, level=logging.ERROR)
    else:
        logger.info(f"Database {operation} on {table or 'unknown'}")
        log_dict(logger, "Database operation details", log_data, level=logging.DEBUG)