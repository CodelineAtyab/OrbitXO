from logging_config import get_logger
from api import call_google_maps
from database import store_record
from notifier import send_notification

app_logger = get_logger("app")

if __name__ == "__main__":
    app_logger.info("Application started")
    call_google_maps()
    store_record()
    send_notification()
    app_logger.info("Application finished")
