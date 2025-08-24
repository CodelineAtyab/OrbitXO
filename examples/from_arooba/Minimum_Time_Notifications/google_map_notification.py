from fastapi import FastAPI, Query
import os
import requests
import dotenv
import json
from datetime import datetime
import schedule
import time
import threading

# Load environment variables
dotenv.load_dotenv()
api_key = os.getenv("MAPS_API_KEY")
slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

app = FastAPI()

# File to store minimum travel times
DATA_FILE = "min_times.json"

# Load saved data on startup
def load_min_times():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Save data to file
def save_min_times(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Stored minimum times
min_times = load_min_times()


@app.get("/travel-time")
def get_travel_time(origin: str = Query(...), destination: str = Query(...)):
    """
    Manual endpoint: returns the current travel time.
    Sends Slack alert only if new record is lower than before.
    """
    return check_route(origin, destination)


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

    response = requests.post(url, headers=headers, json=body)
    data = response.json()

    if "routes" not in data:
        return {"error": data.get("error", {}).get("message", "Unknown error")}

    route = data["routes"][0]
    duration = route["duration"]  # Example: "2700s"
    distance_km = route["distanceMeters"] / 1000

    # Convert seconds to minutes
    duration_minutes = int(duration.replace("s", "")) // 60

    # Key = route (origin->destination)
    key = f"{origin}->{destination}"
    prev_best = min_times.get(key)

    new_record = False
    alert_msg = None

    # Case 1: First time or better record
    if prev_best is None or duration_minutes < prev_best:
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

    # Case 2: Equal or worse -> just update JSON (no Slack)
    else:
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
        print("[WARN] Slack webhook not configured")
        return

    try:
        resp = requests.post(slack_webhook, json={"text": message})
        if resp.status_code == 200:
            print("[INFO] Slack notification sent")
        else:
            print(f"[ERROR] Slack send failed: {resp.text}")
    except Exception as e:
        print(f"[ERROR] Slack exception: {e}")


# =============================
#  Scheduler (Automatic checks)
# =============================

def auto_check():
    """Define the routes you want to monitor automatically."""
    routes = [
        ("Muscat", "Nizwa"),
        ("Home", "Work")  # Example
    ]
    for origin, destination in routes:
        print(f"[AUTO] Checking {origin} -> {destination}")
        check_route(origin, destination)

# Run the auto check every 10 minutes
schedule.every(10).minutes.do(auto_check)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduler in a background thread with FastAPI
threading.Thread(target=run_scheduler, daemon=True).start()
