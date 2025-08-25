"""
Main Application Module

This module demonstrates how to use the logging system
across different components of the application.
"""

import sys
import os

from examples.from_nabil.google_api.logging_implementation import root_logger as logger, set_debug_mode
from api import get_directions
from examples.from_nabil.google_api.notifier import SlackNotifier, EmailNotifier

def main():
    """Main application entry point with comprehensive logging"""
    logger.info("Application starting")
    
    # Check if debug mode is enabled
    if "--debug" in sys.argv:
        set_debug_mode()
        logger.debug("Debug mode enabled")
    
    try:
        # Get directions from API
        logger.info("Requesting directions")
        directions = get_directions("home", "work")
        travel_time = directions["duration"]
        logger.info(f"Retrieved travel time: {travel_time}")
        
        
        # Send notifications
        logger.info("Sending notifications")
        
        # Slack notification
        slack = SlackNotifier("https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX")
        slack_success = slack.send(f"Travel time from home to work is {travel_time}", "#commute-times")
        
        # Email notification
        email = EmailNotifier("smtp.example.com", "notifications@example.com")
        email_success = email.send(
            f"Travel time from home to work is {travel_time}",
            "user@example.com",
            subject="Daily Commute Update"
        )
        
        if not slack_success and not email_success:
            logger.error("All notifications failed to send")
        
        logger.info("Application completed successfully")
        return 0
        
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
