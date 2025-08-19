import os
import json
import requests
from dotenv import load_dotenv
from minimum_time_tracking import check_and_notify_new_minimum

# Load environment variables
load_dotenv()

def get_travel_time_from_google(source, destination, api_key=None):
    if api_key is None:
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not api_key:
            print("Error: Google Maps API key not found")
            return None
    
    # Using the newer Routes API (v2)
    base_url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters"
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
            "avoidFerries": False
        },
        "languageCode": "en-US",
        "units": "METRIC"
    }
    
    try:
        response = requests.post(base_url, headers=headers, json=data)
        response.raise_for_status()
        
        result_data = response.json()
        
        if not result_data.get("routes"):
            print("No routes found in API response")
            return None
            
        # Extract duration in seconds and convert to minutes
        duration_seconds = result_data["routes"][0]["duration"].replace("s", "")
        duration_minutes = float(duration_seconds) / 60
        
        return duration_minutes
        
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {str(e)}")
        return None
    except (KeyError, IndexError, ValueError) as e:
        print(f"Failed to parse API response: {str(e)}")
        return None

def load_locations_from_env():
    """
    Load source and destination locations from environment variables.
    
    Returns:
        tuple: (source, destination) or (None, None) if not found
    """
    source = os.getenv("SOURCE")
    destination = os.getenv("DESTINATION")
    
    if not source or not destination:
        print("Source or destination missing in .env file")
        return None, None
        
    return source, destination

def check_and_update_travel_time():
    """
    Check current travel time using Google Maps API and update minimum time tracking.
    
    Returns:
        dict: Result of check and notification, or None if error
    """
    # Load locations from environment variables
    source, destination = load_locations_from_env()
    if not source or not destination:
        return None
    
    # Get current travel time from Google Maps
    duration_minutes = get_travel_time_from_google(source, destination)
    if not duration_minutes:
        return None
    
    # Round to 1 decimal place for clarity
    duration_minutes = round(duration_minutes, 1)
    print(f"Current travel time from {source} to {destination}: {duration_minutes} minutes")
    
    # Check if it's a new minimum and notify if necessary
    result = check_and_notify_new_minimum(source, destination, duration_minutes)
    return result

# Example usage
if __name__ == "__main__":
    print("Checking current travel time...")
    result = check_and_update_travel_time()
    
    if result:
        if result["new_minimum"]:
            print("\n🎉 NEW MINIMUM TRAVEL TIME DETECTED!")
            print(f"Route: {result['source']} → {result['destination']}")
            print(f"New minimum: {result['current_duration']} minutes")
            print(f"Previous minimum: {result['previous_min']} minutes")
            print(f"Time saved: {result['time_saved']} minutes")
            
            if result["notification_sent"]:
                print("✅ Slack notification sent")
            else:
                print("ℹ️ Notification not sent (cooldown active or webhook not configured)")
        else:
            print("\nNot a new minimum time.")
            print(f"Current: {result['current_duration']} minutes")
            print(f"Minimum: {result['previous_min']} minutes")
    else:
        print("Failed to check travel time")
