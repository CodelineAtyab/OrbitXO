from fastapi import FastAPI, Query
import os
import requests
import dotenv
import json
from datetime import datetime, timedelta
# -------------------------
# Load environment variables
# -------------------------
dotenv.load_dotenv()
API_KEY = os.getenv("MAPS_API_KEY")
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")
app = FastAPI(title="Travel Time Tracker API")
# -------------------------
# Constants and Data Storage
# -------------------------
DATA_FILE = "min_times.json"
COOLDOWN_MINUTES = 30  # Cooldown period to avoid alert fatigue
# Load previous minimum travel times
def load_min_times():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}
# Save minimum travel times to file
def save_min_times(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
min_times = load_min_times()
last_alert_time = {}  # Stores last alert time per route
# -------------------------
# Slack Notification Function
# -------------------------
def send_slack_alert(origin: str, destination: str, duration_minutes: float, prev_best: float, route_key: str):
    """
    Send a visually appealing Slack message for a new minimum travel time.
    Includes emojis and clear formatting.
    """
    now = datetime.now()
    last_time = last_alert_time.get(route_key)
    # Check cooldown
    if last_time and (now - last_time).total_seconds() < COOLDOWN_MINUTES * 60:
        print("[INFO] Cooldown active, skipping Slack alert")
        return
    if not SLACK_WEBHOOK:
        print("[WARN] Slack webhook not configured")
        return
    # Prepare a formatted message with emojis
    time_saved = (prev_best - duration_minutes) if prev_best else 0
    alert_msg = (
        f"*:rotating_light: NEW RECORD TRAVEL TIME! :rotating_light:*\n"
        f"*:motorway: Route:* `{origin} → {destination}`\n"
        f"*:stopwatch: Current estimate:* `{duration_minutes} min`\n"
        f"*:trophy: Previous best:* `{prev_best if prev_best else 'N/A'} min`\n"
        f"*:bulb: Time saved:* `{time_saved} min`\n"
        f"*:date: Recorded at:* `{now.strftime('%Y-%m-%d %H:%M:%S')}`"
    )
    # Send to Slack
    try:
        resp = requests.post(SLACK_WEBHOOK, json={"text": alert_msg})
        if resp.status_code == 200:
            print("[INFO] Slack notification sent :white_check_mark:")
            last_alert_time[route_key] = now
        else:
            print(f"[ERROR] Slack send failed: {resp.text}")
    except Exception as e:
        print(f"[ERROR] Slack exception: {e}")
# -------------------------
# FastAPI Endpoint
# -------------------------
@app.get("/travel-time", summary="Get travel time between two locations")
def get_travel_time(origin: str = Query(..., description="Starting point address"),
                    destination: str = Query(..., description="Destination address")):
    # Check for API key
    if not API_KEY:
        return {"error": "Google Maps API key not configured."}
    # Google Routes API request
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters"
    }
    body = {
        "origin": {"address": origin},
        "destination": {"address": destination},
        "travelMode": "DRIVE"
    }
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    if "routes" not in data or not data["routes"]:
        return {"error": data.get("error", {}).get("message", "Unknown error")}
    route = data["routes"][0]
    duration = route["duration"]
    distance_km = route["distanceMeters"] / 1000
    # Convert duration to minutes
    if isinstance(duration, str) and duration.endswith("s"):
        duration_minutes = round(int(duration.replace("s", "")) / 60, 1)
    else:
        duration_minutes = round(float(duration) / 60, 1)
    # Track minimum travel time
    route_key = f"{origin} → {destination}"
    prev_best = min_times.get(route_key)
    new_record = False
    if prev_best is None or duration_minutes < prev_best:
        min_times[route_key] = duration_minutes
        save_min_times(min_times)
        new_record = True
        # Send enhanced Slack notification
        send_slack_alert(origin, destination, duration_minutes, prev_best, route_key)
    return {
        "origin": origin,
        "destination": destination,
        "duration_minutes": duration_minutes,
        "distance_km": distance_km,
        "new_record": new_record
    }

