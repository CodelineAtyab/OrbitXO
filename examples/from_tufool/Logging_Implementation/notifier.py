import logging
import random

def send_notification(message):
    if random.choice([True, False]):
        logging.warning("Failed to send Slack notification, retrying...")
        # simulate retry
        logging.info("Slack notification sent successfully")
    else:
        logging.info("Slack notification sent successfully")
