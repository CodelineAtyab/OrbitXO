
import logging
import time
logger = logging.getLogger("notifier")

def send_slack_notification(text: str) -> None:
    # Simulate a transient failure then success
    logger.warning("Failed to send Slack notification, retrying...")
    time.sleep(0.1)
    logger.info("Slack notification sent successfully")
