from logging_config import setup_logging
import logging
import api
import database
import notifier

def main():
    setup_logging()
    logging.info("Application started")

    try:
        response = api.call_google_maps_api("home", "work")
        database.save_travel_time(response)
        notifier.send_notification("Travel time is saved.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}", exc_info=True)

if __name__ == "__main__":
    main()
