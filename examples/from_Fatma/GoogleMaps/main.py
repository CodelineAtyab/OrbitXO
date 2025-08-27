import requests
import os
import dotenv
import configparser

# Load environment variables (for the API key)
dotenv.load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Load config (INI format)
config = configparser.ConfigParser()
config.read("application.config")

LOCATIONS = dict(config["locations"])

BASE_URL = "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix"

def get_travel_time(source_key: str, destination_key: str):
    try:
        if source_key not in LOCATIONS or destination_key not in LOCATIONS:
            return f"Invalid source or destination key: {source_key}, {destination_key}"
        
        source = LOCATIONS[source_key]
        destination = LOCATIONS[destination_key]

        body = {
            "origins": [
                {
                    "waypoint": {
                        "address": source
                    }
                }
            ],
            "destinations": [
                {
                    "waypoint": {
                        "address": destination
                    }
                }
            ],
            "travelMode": "DRIVE"
        }

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": API_KEY,
            "X-Goog-FieldMask": "originIndex,destinationIndex,duration,distanceMeters"
        }

        response = requests.post(BASE_URL, headers=headers, json=body)

        if response.status_code != 200:
            return f"HTTP Error {response.status_code}: {response.text}"

        data = response.json()

        if not data or "duration" not in data[0]:
            return "No duration returned from API."

        duration_str = data[0]["duration"]
        duration_sec = int(duration_str.rstrip("s"))
        minutes = duration_sec // 60
        seconds = duration_sec % 60

        if minutes < 60:
            duration_fmt = f"{minutes} min {seconds} sec"
        else:
            hours = minutes // 60
            minutes = minutes % 60
            duration_fmt = f"{hours} hr {minutes} min"

        distance_meters = data[0]["distanceMeters"]
        distance_km = round(distance_meters / 1000, 2)

        return (
            f"Source: {source}\n"
            f"Destination: {destination}\n"
            f"Estimated travel time: {duration_fmt}\n"
            f"Distance: {distance_km} kilometers"
        )

    except requests.exceptions.RequestException as e:
        return f"Network error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

# Example usage
print(get_travel_time("home", "work"))
