import logging
from logging.handlers import TimedRotatingFileHandler
import os
import requests
import json
from dotenv import load_dotenv
from fastapi import FastAPI, Query
import time
# =========================
# Load .env variables
# =========================
load_dotenv()
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
GOOGLE_API_KEY = os.getenv("MAPS_API_KEY")
if not SLACK_WEBHOOK_URL:
    raise ValueError("Slack Webhook URL not found in .env file!")
if not GOOGLE_API_KEY:
    raise ValueError("Google API Key not found in .env file!")
# =========================
# Create directories
# =========================
os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)
# =========================
# Logger Configuration
# =========================
logger = logging.getLogger("Google_Maps_API")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s [%(filename)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler = TimedRotatingFileHandler(
    "logs/Google_Maps_API.log", when="D", interval=1, backupCount=7, encoding="utf-8"
)
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
# =========================
# Slack Notification Function
# =========================
def send_slack_message(message: str):
    payload = {"text": message}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        logger.info(f"Slack message sent: {message}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send Slack message: {e}", exc_info=True)
# =========================
# Google Maps API Call with Retry
# =========================
def fetch_route_with_retry(origin: str, destination: str, retries: int = 3, wait_sec: int = 5):
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters"
    }
    body = {
        "origin": {"address": origin},
        "destination": {"address": destination},
        "travelMode": "DRIVE"
    }
    attempt = 0
    while attempt < retries:
        attempt += 1
        logger.info(f"Attempt {attempt}: Requesting route from {origin} to {destination}")
        logger.debug(f"Request body: {body}")
        try:
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            data = response.json()
            if "routes" in data and len(data["routes"]) > 0:
                route = data["routes"][0]
                logger.info(f"Route found from {origin} to {destination}")
                send_slack_message(f":white_check_mark: Route found from {origin} to {destination}!")
                # Save JSON response
                file_path = f"data/maps_response_{origin}_{destination}.json"
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                logger.info(f"Response saved to {file_path}")
                return {
                    "origin": origin,
                    "destination": destination,
                    "duration": route["duration"],
                    "distance_km": route["distanceMeters"] / 1000
                }
            else:
                logger.warning(f"No routes found from {origin} to {destination}")
                send_slack_message(f":warning: Warning: No routes found from {origin} to {destination}. Retrying...")
                time.sleep(wait_sec)
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}", exc_info=True)
            send_slack_message(f":x: Error: Failed to call Google Maps API: {e}. Retrying...")
            time.sleep(wait_sec)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}", exc_info=True)
            send_slack_message(f":x: Error: Failed to parse response: {e}. Retrying...")
            time.sleep(wait_sec)
    else:
        logger.error(f"All {retries} attempts failed for {origin} to {destination}")
        send_slack_message(f":x: Error: All {retries} attempts failed for route from {origin} to {destination}")
        return {"error": f"No routes found after {retries} attempts"}
# =========================
# List of Available Cities
# =========================
CITIES = ["Muscat", "Fanja", "Seeb", "Nizwa", "Salalah"]
# =========================
# FastAPI Application
# =========================
app = FastAPI(title="Travel Time API", description="Compute driving time between cities in Oman")
@app.get("/travel-time")
def get_travel_time(origin: str = Query(..., description=f"Choose origin from: {CITIES}"),
                    destination: str = Query(..., description=f"Choose destination from: {CITIES}")):
    if origin not in CITIES or destination not in CITIES:
        return {"error": f"Both origin and destination must be in: {CITIES}"}
    return fetch_route_with_retry(origin, destination)
# =========================
# Run FastAPI Server
# =========================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Logging_Implementation:app", host="127.0.0.1", port=8000, reload=True)