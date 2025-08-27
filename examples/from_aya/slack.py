from fastapi import FastAPI, Query
import os
import requests
import dotenv
import logging
from datetime import datetime, timedelta
# Load environment variables from .env file
dotenv.load_dotenv()
# Google Maps API key
api_key = os.getenv("MAPS_API_KEY")
# Slack webhook URL for sending notifications
slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
# Initialize FastAPI app
app = FastAPI()
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
# Dictionary to track the minimum travel time for each route
min_travel_times = {}
# Dictionary to store the last notification time (to prevent spam)
last_notification_time = {}
cooldown_period = timedelta(minutes=30)  # Minimum 30 min between alerts
def send_slack_notification(route, current, previous, saved):
    """
    Send a Slack notification when a new minimum travel time is detected.
    """
    if not slack_webhook:
        logging.warning("Slack webhook is not configured.")
        return
    payload = {
        "text": (
            f":rotating_light: NEW RECORD TRAVEL TIME :rotating_light:\n"
            f"Route: {route}\n"
            f"Current estimate: {current} minutes\n"
            f"Previous best: {previous} minutes\n"
            f"Time saved: {saved} minutes\n"
            f"Recorded at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
    }
    try:
        response = requests.post(slack_webhook, json=payload)
        if response.status_code == 200:
            logging.info("Slack notification sent successfully")
        else:
            logging.error(f"Failed to send Slack notification: {response.text}")
    except Exception as e:
        logging.error(f"Slack notification error: {e}")
@app.get("/travel-time")
def get_travel_time(origin: str = Query(...), destination: str = Query(...)):
    """
    Get travel time and distance between two locations using Google Maps API.
    Also, check if a new minimum travel time is recorded and notify via Slack.
    """
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
    # Call Google Maps API
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    if "routes" not in data:
        return {"error": data.get("error", {}).get("message", "Unknown error")}
    route = data["routes"][0]
    # Convert duration into minutes
    duration_minutes = int(route["duration"].replace("s", "")) // 60
    distance_km = route["distanceMeters"] / 1000
    # Create a key for the route (Origin -> Destination)
    route_key = f"{origin} -> {destination}"
    # Check if this route already has a minimum recorded
    if route_key not in min_travel_times or duration_minutes < min_travel_times[route_key]:
        previous_min = min_travel_times.get(route_key, None)
        min_travel_times[route_key] = duration_minutes
        # Avoid spamming Slack by checking cooldown
        now = datetime.now()
        if (route_key not in last_notification_time or
            now - last_notification_time[route_key] > cooldown_period):
            if previous_min:
                logging.info("New minimum travel time detected!")
                time_saved = previous_min - duration_minutes
                logging.info("Sending Slack notification...")
                send_slack_notification(route_key, duration_minutes, previous_min, time_saved)
            last_notification_time[route_key] = now
    return {
        "origin": origin,
        "destination": destination,
        "duration_minutes": duration_minutes,
        "distance_km": distance_km,
        "minimum_recorded": min_travel_times[route_key]
    }
if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app with autoreload
    uvicorn.run("slack:app", host="127.0.0.1", port=8000, reload=True)