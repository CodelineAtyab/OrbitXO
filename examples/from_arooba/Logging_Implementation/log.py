from fastapi import FastAPI, Query
import os
import requests 
import dotenv
import json
from datetime import datetime
import schedule
import time
import threading
import logging
from logging.handlers import TimedRotatingFileHandler

# ============================= 
# Logging Configuration
# =============================

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("travel_app")
logger.setLevel(logging.DEBUG)  # capture everything

# Rotate logs daily, keep 7 days
handler = TimedRotatingFileHandler(
    filename=os.path.join(LOG_DIR, "travel_time.log"),
    when="midnight",
    backupCount=7,
    encoding="utf-8"
)
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# =============================
# App Configuration
# =============================

dotenv.load_dotenv()
api_key = os.getenv("MAPS_API_KEY")
slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

app = FastAPI()

DATA_FILE = "min_times.json"

def load_min_times():
    logger.info("[database] Loading minimum times from file")
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"[database] Failed to load JSON file: {e}")
    return {}

def save_min_times(data):
    logger.info("[database] Saving minimum times to file")
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        logger.error(f"[database] Failed to save JSON file: {e}")

min_times = load_min_times()

# =============================
# API Endpoint
# =============================

@app.get("/travel-time")
def get_travel_time(origin: str = Query(...), destination: str = Query(...)):
    """
    Manual endpoint: returns the current travel time.
    Sends Slack alert only if new record is lower than before.
    """
    logger.info(f"[api] Received request: origin={origin}, destination={destination}")
    return check_route(origin, destination)


# =============================
# Core Logic
# =============================

def check_route(origin: str, destination: str):
    """Check route travel time and update if it's a new record."""
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters"
    }
    body = {
        "origin": {"address": origin},
        "destination": {"address": destination},
        "travelMode": "DRIVE"
    }

    logger.info("[api] Starting API request to Google Maps")
    logger.debug(f"[api] Request body: {body}")

    try:
        response = requests.post(url, headers=headers, json=body)
        logger.info(f"[api] Google Maps response: {response.status_code}")
        data = response.json()
    except Exception as e:
        logger.error(f"[api] Google Maps request failed: {e}")
        return {"error": str(e)}

    if "routes" not in data:
        logger.warning("[api] No routes found in response")
        return {"error": data.get("error", {}).get("message", "Unknown error")}

    route = data["routes"][0]
    duration = route["duration"]  # Example: "2700s"
    distance_km = route["distanceMeters"] / 1000
    duration_minutes = int(duration.replace("s", "")) // 60

    key = f"{origin}->{destination}"
    prev_best = min_times.get(key)

    new_record = False

    if prev_best is None or duration_minutes < prev_best:
        logger.info(f"[database] New record for {key}: {duration_minutes} minutes (previous {prev_best})")
        min_times[key] = duration_minutes
        save_min_times(min_times)
        new_record = True

        alert_msg = (
            f"🚨 NEW RECORD TRAVEL TIME 🚨\n"
            f"Route: {origin} → {destination}\n"
            f"Current estimate: {duration_minutes} minutes\n"
            f"Previous best: {prev_best if prev_best else 'N/A'} minutes\n"
            f"Time saved: {(prev_best - duration_minutes) if prev_best else 0} minutes\n"
            f"Recorded at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        send_slack_alert(alert_msg)

    else:
        logger.info(f"[database] No new record for {key}: current={duration_minutes}, best={prev_best}")
        min_times[key] = duration_minutes
        save_min_times(min_times)

    return {
        "origin": origin,
        "destination": destination,
        "duration_minutes": duration_minutes,
        "distance_km": distance_km,
        "new_record": new_record
    }


def send_slack_alert(message: str):
    """Send alert to Slack channel using webhook."""
    if not slack_webhook:
        logger.warning("[notifier] Slack webhook not configured")
        return

    try:
        logger.info("[notifier] Sending Slack notification")
        resp = requests.post(slack_webhook, json={"text": message})
        if resp.status_code == 200:
            logger.info("[notifier] Slack notification sent successfully")
        else:
            logger.warning(f"[notifier] Slack send failed: {resp.text}")
    except Exception as e:
        logger.error(f"[notifier] Slack exception: {e}")


# =============================
# Scheduler
# =============================

def auto_check():
    routes = [
        ("Muscat", "Nizwa"),
        ("Home", "Work")
    ]
    for origin, destination in routes:
        logger.info(f"[scheduler] Auto-checking {origin} -> {destination}")
        check_route(origin, destination)
 
schedule.every(10).minutes.do(auto_check)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_scheduler, daemon=True).start()
