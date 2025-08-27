from googleapi_integration import get_travel_time_from_google, check_and_update_travel_time, load_locations_from_env
from minimum_time_tracking import check_and_notify_new_minimum
import logging_implement as logging_impl
import sys
import os
from dotenv import load_dotenv

def setup_environment():
    """Setup environment by loading .env file from the same directory as main.py"""
    base_dir = os.path.dirname(os.path.abspath(__file__))

    logs_dir = os.path.join(base_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    os.environ["LOGS_DIR"] = logs_dir

    logger = logging_impl.get_app_logger("main")
    logger.info(f"Logs directory set to: {logs_dir}")

    env_path = os.path.join(base_dir, ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
        logger.info(f"Loaded environment from {env_path}")
        return True
    else:
        logger.error(f"Environment file not found at {env_path}")
        return False

# We're using load_locations_from_env from googlmap_int.py

def track_travel_time(source, destination):
    logger = logging_impl.get_app_logger("travel_tracker")
    api_logger = logging_impl.get_api_logger("google_maps")

    logger.info(f"Getting travel time from {source} to {destination}")

    api_logger.debug(f"Making Google Maps API call for {source} to {destination}")
    duration_minutes = get_travel_time_from_google(source, destination)

    if duration_minutes is None:
        error_msg = "Failed to get travel time from Google Maps API"
        api_logger.error(error_msg)
        logging_impl.log_google_maps_api_call(
            api_logger, 
            source, 
            destination, 
            error=error_msg
        )
        return None
    else:
        api_logger.info(f"Successful API response received")
        logging_impl.log_google_maps_api_call(
            api_logger,
            source,
            destination,
            duration=duration_minutes
        )

    logger.info(f"Travel time: {duration_minutes} minutes")

    logger.info("Checking if this is a new minimum travel time...")
    tracker_result = check_and_notify_new_minimum(source, destination, duration_minutes)

    if tracker_result["new_minimum"]:
        logger.info(f"New minimum travel time detected: {tracker_result['current_duration']} minutes")
        logger.info(f"Previous minimum: {tracker_result['previous_min']} minutes")
        logger.info(f"Time saved: {tracker_result['time_saved']} minutes")

        if tracker_result["notification_sent"]:
            logger.info("Slack notification sent successfully")
        else:
            logger.warning("Slack notification was not sent (cooldown active or webhook not configured)")
    else:
        logger.info(f"Not a new minimum. Current: {tracker_result['current_duration']} minutes, Minimum: {tracker_result['previous_min']} minutes")

    return {
        "duration_minutes": duration_minutes,
        "tracker_result": tracker_result
    }

def main():
    logger = logging_impl.get_app_logger("main")

    logger.info("Starting travel time tracker")

    if not setup_environment():
        logger.error("Failed to setup environment")
        return 1

    try:
        try:
            source, destination = load_locations_from_env()
            if not source or not destination:
                logger.error("SOURCE and DESTINATION must be defined in .env file")
                return 1

            logger.info(f"Loaded locations: {source} to {destination}")
        except Exception as e:
            logger.error(f"Error loading locations: {e}")
            return 1

        # Option 1: Use the integrated function in googlmap_int.py
        logger.info("Using integrated check_and_update_travel_time from googlmap_int...")
        integrated_result = check_and_update_travel_time()

        if integrated_result:
            logger.info(f"Check complete. Current travel time: {integrated_result['current_duration']} minutes")

            if integrated_result['new_minimum']:
                logger.info("New minimum detected!")

            # We can also use our detailed tracking function for more logging
            result = track_travel_time(source, destination)

            if result:
                logger.info("Travel time tracking completed successfully")
                logging_impl.log_dict(logger, "Final results", result)
                return 0
        else:
            logger.error("Failed to track travel time")
            return 1

    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())