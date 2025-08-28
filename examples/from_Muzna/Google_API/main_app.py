import os
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Union
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn
import httpx
from tinydb import TinyDB, Query
from fastapi.responses import FileResponse

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
app = FastAPI(title="Live Travel Time & Route Manager")

# Mount the current directory to serve static files (like index.html)
app.mount("/static", StaticFiles(directory=".", html=True), name="static")

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
NOTIFICATION_COOLDOWN_MINUTES = 60
CONFIG_FILE = "routes.json"

db = TinyDB('db.json')
travel_records_table = db.table('travel_records')
notifications_table = db.table('notifications')
Route = Query()

# --- CORS Middleware ---
# This middleware allows your front-end (from any origin) to
# make requests to this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)

# --- Pydantic Models ---
# Model for the travel time request
class TravelRequest(BaseModel):
    source_address: str
    destination_address: str

# Model for a single route entry (for JSON file)
class RouteEntry(BaseModel):
    name: str
    source_address: str
    destination_address: str

# Model for the request body when adding a new route.
class AddRouteRequest(BaseModel):
    route_name: str
    source_address: str
    destination_address: str

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- Helper Functions for Route Management ---
def load_routes():
    """Loads existing routes from the configuration file."""
    if not os.path.exists(CONFIG_FILE):
        return []
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        logging.error(f"Failed to load routes from {CONFIG_FILE}: {e}")
        return []

def save_routes(routes: List[Dict]):
    """Saves the current list of routes to the configuration file."""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(routes, f, indent=4)
    except IOError as e:
        logging.error(f"Failed to save routes to {CONFIG_FILE}: {e}")

# --- Core Functions for Travel Time & Notifications ---
async def send_slack_notification(source_address: str, destination_address: str, current_duration_min: int, prev_best_min: int):
    """Sends a formatted notification to a Slack channel."""
    if not SLACK_WEBHOOK_URL:
        logging.error("Slack Webhook URL is not configured.")
        return

    time_saved = prev_best_min - current_duration_min
    
    message = {
        "text": f"NEW RECORD TRAVEL TIME: {source_address} → {destination_address}",
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
                {"type": "mrkdwn", "text": f"*Route:*\n{source_address} → {destination_address}"},
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

# --- API Endpoints ---
@app.get("/")
async def read_index():
    return FileResponse("index.html")

@app.get("/routes", response_model=List[RouteEntry], summary="Get all routes")
async def get_routes():
    """Returns the list of all configured routes."""
    return load_routes()

@app.post("/add-route", response_model=Dict[str, str], status_code=201, summary="Add a new route")
async def add_route(request: AddRouteRequest):
    """Adds a new source-destination pair to the configuration."""
    routes = load_routes()
    # Check for duplicate route names
    if any(route['name'].lower() == request.route_name.lower() for route in routes):
        raise HTTPException(status_code=400, detail=f"Route with name '{request.route_name}' already exists.")

    new_route = {
        "name": request.route_name,
        "source_address": request.source_address,
        "destination_address": request.destination_address
    }
    routes.append(new_route)
    save_routes(routes)
    return {"status": "Route added successfully."}

@app.delete("/remove-route/{route_name}", response_model=Dict[str, str], summary="Remove a route")
async def remove_route(route_name: str):
    """Removes a route by its name from the configuration."""
    routes = load_routes()
    original_count = len(routes)
    routes = [route for route in routes if route['name'] != route_name]

    if len(routes) == original_count:
        raise HTTPException(status_code=404, detail=f"Route with name '{route_name}' not found.")
        
    save_routes(routes)
    return {"status": "Route removed successfully."}

@app.post("/check-travel-time")
async def check_travel_time(request: TravelRequest):
    # Access the properties from the Pydantic model
    source_address = request.source_address
    destination_address = request.destination_address

    route_key = f"{source_address.replace(' ', '')}-{destination_address.replace(' ', '')}"

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
            logging.info(f"Cooldown active. Notification for {route_key} suppressed until {cooldown_end_time.strftime('%H:%M:%S')}")
        else:
            logging.info("Sending Slack notification...")
            
            # Use the previous best for the "time saved" calculation
            previous_best_minutes = (previous_best_seconds // 60) if previous_best_seconds else (current_duration_minutes + 5)
            
            await send_slack_notification(
                source_address=source_address,
                destination_address=destination_address,
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