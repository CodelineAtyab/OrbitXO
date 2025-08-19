import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read API key from .env
API_KEY = os.getenv("GOOGLE_API_KEY")

# Define saved locations directly in the code
saved_locations = {
    "home": "123 Home Alansab, Muscat, Oman",
    "work": "456 Office Codeline, Muscat, Oman",
    "gym": "789 Gym Bowsher, Muscat, Oman"
}

def get_travel_time(source_key, destination_key):
    if source_key not in saved_locations or destination_key not in saved_locations:
        print("Error: One or both location keys are invalid.")
        return

    origin = saved_locations[source_key]
    destination = saved_locations[destination_key]

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

    try:
        response = requests.post(url, headers=headers, json=body)

        # Debugging info
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)

        if response.status_code != 200:
            print("API Error:", response.text)
            return

        data = response.json()
        route = data["routes"][0]

        duration = route["duration"]
        distance = route["distanceMeters"]

        print(f" Source: {origin}")
        print(f" Destination: {destination}")
        print(f" Estimated travel time: {duration}")
        print(f" Distance: {distance/1000:.2f} km")

    except requests.RequestException as e:
        print(f"Network Error: {e}")


# Example usage
get_travel_time("home", "work")
