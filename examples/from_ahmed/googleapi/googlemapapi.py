import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()


def get_travel_time(source, destination, api_key=None):
    if api_key is None:
        try:
            # Try to load from config.json first
            with open("config.json", "r") as f:
                config = json.load(f)
                api_key = config.get("api_key")
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            # If config.json fails, try environment variable
            api_key = os.getenv("GOOGLE_MAPS_API_KEY")

        if not api_key:
            raise ValueError(
                "No Google Maps API key found. Please provide it as a parameter, in config.json, or as GOOGLE_MAPS_API_KEY environment variable."
            )

    base_url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.legs.steps.travelAdvisory",
    }
    data = {
        "origin": {"address": source},
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
        "units": "METRIC",
    }
    try:
        response = requests.post(base_url, headers=headers, json=data)
        response.raise_for_status()
        result_data = response.json()
        if not result_data.get("routes"):
            raise ValueError(f"No routes found for {source} to {destination}")

        route = result_data["routes"][0]
        duration_seconds = int(route["duration"][:-1])  # Remove the 's' from the duration string
        duration_minutes = round(duration_seconds / 60)
        distance_meters = int(route["distanceMeters"])
        distance_km = round(distance_meters / 1000, 1)

        return {
            "duration_seconds": duration_seconds,
            "duration_minutes": duration_minutes,
            "distance_meters": distance_meters,
            "distance_km": distance_km,
        }
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Request to Google Maps API failed: {str(e)}")
    except (KeyError, IndexError, ValueError) as e:
        raise ValueError(f"Failed to parse Google Maps API response: {str(e)}")


def load_locations_from_config(config_path):
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            source = config.get("source")
            destination = config.get("destination")
            api_key = config.get("api_key")
            return source, destination, api_key
    except (json.JSONDecodeError, FileNotFoundError) as e:
        raise ValueError(f"Failed to load config from {config_path}: {str(e)}")


if __name__ == "__main__":
    try:
        # Example usage
        source, destination, api_key = load_locations_from_config("config.json")
        result = get_travel_time(source, destination, api_key)
        print(f"Travel time from {source} to {destination}:")
        print(f"Duration: {result['duration_minutes']} minutes")
        print(f"Distance: {result['distance_km']} km")
    except Exception as e:
        print(f"Error: {str(e)}")