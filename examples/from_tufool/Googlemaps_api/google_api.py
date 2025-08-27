import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_address(key):
    return os.getenv(key.upper())  # e.g., HOME, WORK

def get_travel_time(source_key, dest_key):
    api_key = os.getenv("MAP_API_KEY")

    origin = get_address(source_key)
    destination = get_address(dest_key)

    if not origin or not destination:
        return f"Invalid source or destination: {source_key}, {dest_key}"

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

    try:
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()

        if "routes" not in data or not data["routes"]:
            return "No route found in response."

        route = data["routes"][0]
        duration_text = route["duration"]
        distance_meters = route["distanceMeters"]

        # duration is an ISO 8601 duration like "1234s", extract seconds
        duration_seconds = int(duration_text.replace("s", ""))

        return f"""Source: {origin}
Destination: {destination}
Estimated travel time: {duration_seconds // 60} minutes
Distance: {distance_meters / 1000:.2f} kilometers"""

    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

# Run directly
if __name__ == "__main__":
    result = get_travel_time("home", "work")
    print(result)
