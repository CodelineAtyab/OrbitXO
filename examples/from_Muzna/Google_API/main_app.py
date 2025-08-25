import os
import logging
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import uvicorn
import httpx
from tinydb import TinyDB, Query

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
app = FastAPI()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
NOTIFICATION_COOLDOWN_MINUTES = 60
LOCATIONS = {
    "home": "Muscat Grand Mall, Muscat, Oman",
    "work": "salalah, Oman"
}

db = TinyDB('db.json')
travel_records_table = db.table('travel_records')
notifications_table = db.table('notifications')
Route = Query()

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# --- Core Functions ---
async def send_slack_notification(route_key: str, current_duration_min: int, prev_best_min: int):
    """Sends a formatted notification to a Slack channel."""
    if not SLACK_WEBHOOK_URL:
        logging.error("Slack Webhook URL is not configured.")
        return

    source, destination = route_key.split('-')
    time_saved = prev_best_min - current_duration_min
    
    message = {
        "text": f"NEW RECORD TRAVEL TIME: {source.title()} → {destination.title()}",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🚨 New Record Travel Time! 🚨"
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Route:*\n{source.title()} → {destination.title()}"},
                    {"type": "mrkdwn", "text": f"*Time Saved:*\n*{time_saved} minute(s)*"},
                    {"type": "mrkdwn", "text": f"*Current Estimate:*\n{current_duration_min} minutes"},
                    {"type": "mrkdwn", "text": f"*Previous Best:*\n{prev_best_min} minutes"},
                ]
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": f"Recorded at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                        "emoji": True
                    }
                ]
            }
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(SLACK_WEBHOOK_URL, json=message)
            response.raise_for_status()
        logging.info("Slack notification sent successfully.")
    except httpx.HTTPError as e:
        logging.error(f"Failed to send Slack notification: {e}")

async def get_live_travel_time(source_addr: str, dest_addr: str) -> int | None:
    """Fetches live travel time from Google Maps using the Routes API."""
    if not API_KEY:
        logging.error("Google Maps API key is missing.")
        return None
        
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "routes.duration"
    }
    payload = {
        "origin": {"address": source_addr},
        "destination": {"address": dest_addr},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE"
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if "routes" in data and len(data["routes"]) > 0:
                duration_str = data["routes"][0]["duration"]
                return int(duration_str.rstrip('s'))
            else:
                logging.warning("No routes found in Google Maps API response.")
                return None
    except httpx.HTTPError as e:
        logging.error(f"Google Maps API request failed: {e}")
        return None
    except (KeyError, IndexError) as e:
        logging.error(f"Could not parse Google Maps API response: {e}")
        return None

# @app.get("/test-notification")
# async def test_notification():
#     await send_slack_notification(
#         route_key="home-work",
#         current_duration_min=12,
#         prev_best_min=15
#     )
#     return {"status": "Test Slack notification sent"}

@app.post("/check-travel-time")
async def check_travel_time(source: str, destination: str):
    """Main endpoint to check and log travel time."""
    if source not in LOCATIONS or destination not in LOCATIONS:
        raise HTTPException(status_code=400, detail="Invalid source or destination.")

    source_address = LOCATIONS[source]
    destination_address = LOCATIONS[destination]
    route_key = f"{source}-{destination}"
    
    # Check for existing record in the database
    record = travel_records_table.get(Route.route_key == route_key)
    previous_best_seconds = record['duration_seconds'] if record else None
    
    current_duration_seconds = await get_live_travel_time(source_address, destination_address)
    
    if current_duration_seconds is None:
        return {"status": "Failed to fetch travel time from Google Maps."}
    
    current_duration_minutes = current_duration_seconds // 60
    
    prev_min_display = f"{previous_best_seconds // 60} mins" if previous_best_seconds else "N/A"
    logging.info(f"Route: {route_key.upper()} | Current: {current_duration_minutes} mins | Record: {prev_min_display}")

    # Check for a new minimum travel time
    if previous_best_seconds is None or current_duration_seconds < previous_best_seconds:
        logging.info(f"New minimum travel time detected for {route_key}!")
        
        # Check cooldown status from the database
        last_notification_rec = notifications_table.get(Route.route_key == route_key)
        last_notified = datetime.fromisoformat(last_notification_rec['timestamp']) if last_notification_rec else None
        
        cooldown_end_time = last_notified + timedelta(minutes=NOTIFICATION_COOLDOWN_MINUTES) if last_notified else None

        if cooldown_end_time and datetime.now() < cooldown_end_time:
            logging.info(f"Cooldown active. Notification for {route_key} suppressed until {cooldown_end_time.strftime('%H:%M:%S')}.")
        else:
            logging.info("Sending Slack notification...")
            
            # Use the previous best for the "time saved" calculation
            previous_best_minutes = (previous_best_seconds // 60) if previous_best_seconds else (current_duration_minutes + 5)
            
            await send_slack_notification(
                route_key=route_key,
                current_duration_min=current_duration_minutes,
                prev_best_min=previous_best_minutes
            )
            # Update the notification timestamp in the database
            notifications_table.upsert({'route_key': route_key, 'timestamp': datetime.now().isoformat()}, Route.route_key == route_key)

        # Update the travel record in the database
        travel_records_table.upsert({'route_key': route_key, 'duration_seconds': current_duration_seconds}, Route.route_key == route_key)
        
        return {"status": "New minimum recorded.", "current_minutes": current_duration_minutes}
    else:
        return {"status": "No new minimum detected.", "current_minutes": current_duration_minutes, "record_minutes": previous_best_seconds // 60}

# --- Local Run ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)