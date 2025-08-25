from googlemapapi import get_travel_time, load_locations_from_config
import timetracker
import Logging_Implementation
import sys
import os
import dotenv
from connection_module import get_db_connector

def setup_environment():
    """Setup environment by loading .env file from the same directory as main.py"""
    base_dir = os.path.dirname(os.path.abspath(__file__))

    logs_dir = os.path.join(base_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    os.environ["LOGS_DIR"] = logs_dir

    logger = Logging_Implementation.get_app_logger("main")
    logger.info(f"Logs directory set to: {logs_dir}")

    env_path = os.path.join(base_dir, ".env")
    if os.path.exists(env_path):
        dotenv.load_dotenv(env_path)
        logger.info(f"Loaded environment from {env_path}")
        return True
    else:
        logger.error(f"Environment file not found at {env_path}")
        return False

def load_locations_from_env():
    """Load locations from environment variables"""
    source = os.environ.get("SOURCE")
    destination = os.environ.get("DESTINATION")

    if not source or not destination:
        raise ValueError("SOURCE and DESTINATION must be defined in .env file")

    return source, destination

def track_travel_time(source, destination):
    logger = Logging_Implementation.get_app_logger("travel_tracker")
    api_logger = Logging_Implementation.get_api_logger("google_maps")

    logger.info(f"Getting travel time from {source} to {destination}")

    api_logger.debug(f"Making Google Maps API call for {source} to {destination}")
    travel_result = get_travel_time(source, destination)

    if not travel_result["success"]:
        api_logger.error(f"Failed to get travel time: {travel_result['error']}")
        api_logger.debug(f"Error details: {travel_result.get('details', 'No details provided')}")
        return None
    else:
        api_logger.info(f"Successful API response received")
        api_logger.debug(f"API response: {travel_result}")

    duration_minutes = travel_result["duration_value"] // 60

    logger.info(f"Travel time: {travel_result['duration']} ({duration_minutes} minutes)")
    logger.info(f"Distance: {travel_result['distance']}")


    db = get_db_connector()
    is_recorded = db["add_travel_time_record"](
        source=source,
        destination=destination,
        duration_minutes=duration_minutes,
        distance=travel_result["distance"],
        distance_value=travel_result.get("distance_value")
    )

    if is_recorded:
        logger.info("Travel time recorded in database")
    else:
        logger.warning("Failed to record travel time in database")

    logger.info("Checking if this is a new minimum travel time...")
    tracker_result = timetracker.check_and_notify_new_minimum(source, destination, duration_minutes)

    if tracker_result["new_minimum"]:
        logger.info(f"New minimum travel time detected: {tracker_result['current_duration']} minutes")
        logger.info(f"Previous minimum: {tracker_result['previous_min']} minutes")
        logger.info(f"Time saved: {tracker_result['time_saved']} minutes")


        db["add_travel_time_record"](
            source=source,
            destination=destination,
            duration_minutes=duration_minutes,
            distance=travel_result["distance"],
            distance_value=travel_result.get("distance_value"),
            is_minimum=True
        )

        if tracker_result["notification_sent"]:
            logger.info("Slack notification sent successfully")
        else:
            logger.warning("Slack notification was not sent (cooldown active or webhook not configured)")
    else:
        logger.info(f"Not a new minimum. Current: {tracker_result['current_duration']} minutes, Minimum: {tracker_result['previous_min']} minutes")

    return {
        "travel_result": travel_result,
        "tracker_result": tracker_result
    }

def main():
    logger = Logging_Implementation.get_app_logger("main")

    logger.info("Starting travel time tracker")

    if not setup_environment():
        logger.error("Failed to setup environment")
        return 1

    try:
        try:
            source, destination = load_locations_from_env()
            logger.info(f"Loaded locations: {source} to {destination}")
        except ValueError as e:
            logger.error(f"Error loading locations: {e}")
            return 1

        result = track_travel_time(source, destination)

        if result:
            logger.info("Travel time tracking completed successfully")
            Logging_Implementation.log_dict(logger, "Final results", result)
            return 0
        else:
            logger.error("Failed to track travel time")
            return 1

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())