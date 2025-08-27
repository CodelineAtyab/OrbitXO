import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_travel_time(source, destination, api_key=None):
    if api_key is None:
        # First try to get API key from environment variable
        api_key = os.environ.get("API_KEY")
        
        if not api_key or api_key == "YOUR_GOOGLE_MAPS_API_KEY":
            # For testing/demo purposes, just return a mock response
            return {
                "success": False,
                "error": "API key not configured",
                "details": "API key is not set in the .env file"
            }
    
    base_url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.legs.steps.travelAdvisory"
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
        try:
            response = requests.post(base_url, headers=headers, json=data, timeout=5)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timed out",
                "details": "The API request took too long to respond"
            }
        
        result_data = response.json()
        
        if not result_data.get("routes"):
            return {
                "success": False,
                "error": "No routes found",
                "details": "The API could not find a route between the specified locations"
            }
        
        route = result_data["routes"][0]
        duration_seconds = int(route["duration"].rstrip("s"))
        distance_meters = route["distanceMeters"]
        
        hours, remainder = divmod(duration_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            duration_text = f"{hours} hour{'s' if hours > 1 else ''}"
            if minutes > 0:
                duration_text += f" {minutes} min"
        else:
            duration_text = f"{minutes} min"
        
        distance_km = distance_meters / 1000
        distance_text = f"{distance_km:.1f} km"
        
        result = {
            "success": True,
            "source": source,
            "destination": destination,
            "distance": distance_text,
            "distance_value": distance_meters,
            "duration": duration_text,
            "duration_value": duration_seconds
        }
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": "Request failed",
            "details": str(e)
        }
    except (KeyError, IndexError, ValueError) as e:
        return {
            "success": False,
            "error": "Failed to parse API response",
            "details": str(e)
        }

def load_locations_from_config(config_path=None):
    # We're not using config_path anymore, but keeping the parameter for compatibility
    try:
        # Ensure .env is loaded
        load_dotenv()
        
        source = os.environ.get("SOURCE")
        destination = os.environ.get("DESTINATION")
        
        if not source or not destination:
            raise ValueError("Source or destination missing in .env file")
            
        return source, destination
    
    except Exception as e:
        raise ValueError(f"Error loading environment variables: {str(e)}")

if __name__ == "__main__":
    try:
        source, destination = load_locations_from_config()
        
        result = get_travel_time(source, destination)
            
    except Exception as e:
        pass