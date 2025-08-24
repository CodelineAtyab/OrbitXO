import os
import json
import requests
from dotenv import load_dotenv
from minimum_time_tracking import check_and_notify_new_minimum

# Load environment settings
load_dotenv()

def fetch_travel_time(origin: str, destination: str, api_key: str | None = None) -> float | None:
    """
    Call Google Maps Routes API (v2) and return travel time in minutes.
    """
    key = api_key or os.getenv("GOOGLE_MAPS_API_KEY")
    if not key:
        print("❌ Missing Google Maps API key")
        return None

    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": key,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters"
    }

    payload = {
        "origin": {"address": origin},
        "destination": {"address": destination},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
        "computeAlternativeRoutes": False,
        "routeModifiers": {
            "avoidTolls": False,
            "avoidHighways": False,
            "avoidFerries": False,
        },
        "languageCode": "en-US",
        "units": "METRIC"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        routes = data.get("routes")
        if not routes:
            print("⚠️ No routes available in response")
            return None

        # Extract "123s" → 123 seconds → minutes
        raw_duration = routes[0]["duration"].replace("s", "")
        minutes = float(raw_duration) / 60
        return minutes

    except requests.exceptions.RequestException as e:
        print(f"❌ API call error: {e}")
    except (KeyError, ValueError, IndexError) as e:
        print(f"⚠️ Problem parsing response: {e}")

    return None


def read_locations() -> tuple[str | None, str | None]:
    """
    Pull origin/destination from .env file.
    """
    origin = os.getenv("SOURCE")
    destination = os.getenv("DESTINATION")

    if not origin or not destination:
        print("⚠️ SOURCE or DESTINATION not set in .env")
        return None, None

    return origin, destination


def evaluate_travel_time() -> dict | None:
    """
    Fetch current travel time and update minimum records.
    """
    origin, destination = read_locations()
    if not origin or not destination:
        return None

    minutes = fetch_travel_time(origin, destination)
    if minutes is None:
        return None

    minutes = round(minutes, 1)
    print(f"🛣️ Travel time {origin} → {destination}: {minutes} minutes")

    return check_and_notify_new_minimum(origin, destination, minutes)


if __name__ == "__main__":
    print("🔎 Checking travel time...")
    result = evaluate_travel_time()

    if not result:
        print("❌ Could not determine travel time")
    elif result["new_minimum"]:
        print("\n🎉 New record low travel time!")
        print(f"Route: {result['source']} → {result['destination']}")
        print(f"⏱️ New: {result['current_duration']} min | Old: {result['previous_min']} min")
        print(f"💡 Saved: {result['time_saved']} min")
        print("✅ Slack notification sent" if result["notification_sent"] else "ℹ️ No notification sent")
    else:
        print("\nNo new minimum.")
        print(f"Now: {result['current_duration']} min | Best: {result['previous_min']} min")
