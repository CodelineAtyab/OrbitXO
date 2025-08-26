import logging
import os
from uuid import uuid4

# Direct imports (no dots)
from logging_setup import setup_logging
from utils import request_context
from api import get_travel_time
from database import store_travel_time
from notifier import send_slack_notification

def run_demo():
    # Initialize logging
    setup_logging()
    app_logger = logging.getLogger("app")

    # App start
    app_logger.info("Application started")

    # Use request context (adds request_id and user to logs)
    with request_context(request_id=str(uuid4()), user=os.getenv("USER", "dev")):
        try:
            # Call API
            minutes = get_travel_time("home", "work")

            # Store in database
            store_travel_time(minutes)

            # Send notification
            send_slack_notification(f"Latest commute time: {minutes} minutes")

        except Exception:
            app_logger.exception("Top-level error while processing request")

    app_logger.info("Application finished")

if __name__ == "__main__":
    run_demo()
