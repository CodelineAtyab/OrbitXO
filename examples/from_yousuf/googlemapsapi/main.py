import os
from googlemapapi import get_travel_time, load_locations_from_config
from timetracker import check_and_notify_new_minimum
from logger import configure_logging, get_logger

configure_logging(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = get_logger(__name__)

def main():
    source, destination = load_locations_from_config()
    result = get_travel_time(source, destination)
    if not result.get("success"):
        logger.error("Error: %s", result.get("error"))
        logger.debug("Details: %s", result.get("details"))
        return 1
    
    duration_seconds = result.get("duration_value", 0)
    duration_minutes = int(round(duration_seconds / 60)) if duration_seconds else 0
    logger.info("Travel from %s to %s:", result['source'], result['destination'])
    logger.info("Distance: %s", result['distance'])
    logger.info("Duration: %s (%d minutes)", result['duration'], duration_minutes)
    update_result = check_and_notify_new_minimum(result['source'], result['destination'], duration_minutes)
    if update_result.get("new_minimum"):
        logger.info("New minimum recorded.")
        if update_result.get("notification_sent"):
            logger.info("Notification sent.")
        else:
            logger.warning("Notification not sent (cooldown or webhook not configured).")
    else:
        logger.info("No new minimum.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
