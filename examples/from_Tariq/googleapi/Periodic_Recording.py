import time
import schedule
import threading
import os
import sys
import datetime
import Logging_Implementation
from googlemapapi import get_travel_time
from connection_module import get_db_connector

_logger = None
_api_logger = None
_db = None
_running = False
_thread = None
_routes = []

def init_loggers():
    global _logger, _api_logger
    _logger = Logging_Implementation.get_app_logger("scheduler")
    _api_logger = Logging_Implementation.get_api_logger("scheduler_api")

def init_db():
    global _db
    _db = get_db_connector()

def add_route(source, destination):
    global _routes, _logger
    
    if _logger is None:
        init_loggers()
        
    _routes.append({
        "source": source,
        "destination": destination
    })
    _logger.info(f"Added route: {source} to {destination}")

def record_travel_time(source, destination):
    global _logger, _api_logger, _db
    
    if _logger is None:
        init_loggers()
    
    if _db is None:
        init_db()
        
    _logger.info(f"Recording travel time: {source} to {destination}")
    
    try:
        _api_logger.debug(f"Making Google Maps API call for {source} to {destination}")
        travel_result = get_travel_time(source, destination)
        
        if not travel_result["success"]:
            _api_logger.error(f"Failed to get travel time: {travel_result['error']}")
            return False
            
        duration_minutes = travel_result["duration_value"] // 60
        distance = travel_result["distance"]
        distance_value = travel_result.get("distance_value")
        
        min_times = _db["get_minimum_travel_times"](source, destination)
        is_minimum = False
        
        if not min_times or duration_minutes < min_times[0].get("min_duration", float('inf')):
            is_minimum = True
            _logger.info(f"New minimum travel time detected: {duration_minutes} minutes")
        
        success = _db["add_travel_time_record"](
            source=source,
            destination=destination,
            duration_minutes=duration_minutes,
            distance=distance,
            distance_value=distance_value,
            is_minimum=is_minimum
        )
        
        if success:
            _logger.info(f"Recorded travel time: {source} to {destination}, {duration_minutes} minutes")
        
        return success
        
    except Exception as e:
        _logger.error(f"Error recording travel time: {e}")
        return False

def record_all_routes():
    global _routes, _logger
    
    if _logger is None:
        init_loggers()
        
    _logger.info(f"Recording travel times for {len(_routes)} routes")
    
    for route in _routes:
        record_travel_time(route["source"], route["destination"])

def scheduler_loop():
    global _running, _logger
    
    if _logger is None:
        init_loggers()
        
    _logger.info("Scheduler loop started")
    
    while _running:
        schedule.run_pending()
        time.sleep(1)
        
    _logger.info("Scheduler loop stopped")

def start_scheduler(interval_minutes=15):
    global _running, _thread, _routes, _logger
    
    if _logger is None:
        init_loggers()
    
    if _running:
        _logger.warning("Scheduler is already running")
        return False
        
    if not _routes:
        _logger.warning("No routes configured for monitoring")
        return False
        
    _running = True
    
    schedule.every(interval_minutes).minutes.do(record_all_routes)
    _logger.info(f"Scheduled travel time recording every {interval_minutes} minutes")
    
    record_all_routes()
    
    _thread = threading.Thread(target=scheduler_loop)
    _thread.daemon = True
    _thread.start()
    
    _logger.info("Travel time scheduler started")
    return True

def stop_scheduler():
    global _running, _thread, _logger
    
    if _logger is None:
        init_loggers()
        
    if not _running:
        _logger.warning("Scheduler is not running")
        return
        
    _running = False
    
    if _thread:
        _thread.join(timeout=10)
        
    schedule.clear()
    _logger.info("Travel time scheduler stopped")

def run_travel_time_scheduler(sources_destinations, interval_minutes=15):
    global _logger
    
    _logger = Logging_Implementation.get_app_logger("scheduler_runner")
    _logger.info(f"Setting up travel time scheduler with {len(sources_destinations)} routes")
    
    init_loggers()
    init_db()
    
    for source, destination in sources_destinations:
        add_route(source, destination)
    
    success = start_scheduler(interval_minutes)
    
    if success:
        _logger.info(f"Travel time scheduler started successfully, recording every {interval_minutes} minutes")
        return {
            "start": start_scheduler,
            "stop": stop_scheduler,
            "add_route": add_route,
            "record_now": record_all_routes
        }
    else:
        _logger.error("Failed to start travel time scheduler")
        return None