import requests
import json
import os

def get_travel_time(source, destination, api_key=None):
    if api_key is None:
        try:
            with open("config.json", 'r') as f:
                config = json.load(f)
                api_key = config.get("api_key")
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
        
        if not api_key:
            raise ValueError("Google Maps API key not found in config file or environment variables")
    
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

def load_locations_from_config(config_path):
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        source = config.get("source")
        destination = config.get("destination")
        
        if not source or not destination:
            raise ValueError("Source or destination missing in config file")
            
        return source, destination
    
    except (json.JSONDecodeError, FileNotFoundError) as e:
        raise ValueError(f"Error loading config file: {str(e)}")

if __name__ == "__main__":
    try:
        config_path = "config.json"
        source, destination = load_locations_from_config(config_path)
        
        result = get_travel_time(source, destination)
            
    except Exception as e:
        pass