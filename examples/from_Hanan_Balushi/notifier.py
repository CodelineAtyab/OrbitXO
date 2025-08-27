from logging_config import log_setup
import random

log = log_setup("notifier")

def send_slack_notification(message):
    try:
        # Simulation of possible failure
        if random.choice([True, False]):
            raise Exception("Slack API Timeout")
        log.info("Slack notification sent successfully")
    except Exception as e:
        log.warning(f"Failed to send Slack notification, retrying... ({e})")