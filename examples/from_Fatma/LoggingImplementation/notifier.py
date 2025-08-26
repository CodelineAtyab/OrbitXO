from logging_config import get_logger
notifier_logger = get_logger("notifier")

def send_notification():
    notifier_logger.warning("Failed to send Slack notification, retrying...")
    notifier_logger.info("Slack notification sent successfully")
