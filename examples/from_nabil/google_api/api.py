import json
import requests
import os
import sys
from dotenv import load_dotenv
def get_travel_time(source, destination, api_key=None):
    if api_key is None:
        load_dotenv()
        api_key = os.environ.get("GOOGLE_MAPS_API_KEY")

        if not api_key:
            raise ValueError("Google Maps API key not found in environment variables")
    
    # Use the Routes API with the correct request format
    base_url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    
    # Build the request body for the Routes API
    request_body = {
        "origin": {
            "address": source
        },
        "destination": {
            "address": destination
        },
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
    
    # Set the required headers
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"
    }

    try:
        # Use POST instead of GET for the Routes API
        response = requests.post(base_url, json=request_body, headers=headers)
        
        # Handle HTTP errors
        if response.status_code != 200:
            error_data = response.json() if response.content else {"error": "Unknown error"}
            error_message = error_data.get("error", {}).get("message", "Unknown error")
            error_status = error_data.get("error", {}).get("status", str(response.status_code))
            
            return {
                "success": False,
                "error": f"API error: {error_status}",
                "details": error_message
            }
            
        data = response.json()
        
        # Check if routes exist in the response
        if "routes" not in data or not data["routes"]:
            return {
                "success": False,
                "error": "API error: No routes found",
                "details": "The API did not return any routes between the specified locations"
            }
        
        # Extract the route information
        route = data["routes"][0]
        
        # Format duration
        duration_seconds = int(route.get("duration", "0").rstrip("s"))
        minutes, seconds = divmod(duration_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours > 0:
            duration_text = f"{hours} hour{'s' if hours > 1 else ''} {minutes} min"
        else:
            duration_text = f"{minutes} min"
            
        # Format distance
        distance_meters = int(route.get("distanceMeters", 0))
        if distance_meters >= 1000:
            distance_text = f"{distance_meters/1000:.1f} km"
        else:
            distance_text = f"{distance_meters} m"
        
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
    
def load_locations_from_config(config_paths=None):
    """
    Attempt to load configuration from multiple possible file paths.
    Returns source, destination, and api_key if found.
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    if config_paths is None:
        # Try several possible config file locations
        config_paths = [
            os.path.join(script_dir, "config.json"),             # google_api/config.json
            os.path.join(script_dir, "google_map_api.json"),     # google_api/google_map_api.json
            os.path.join(parent_dir, "google_map_api.json")      # from_nabil/google_map_api.json
        ]
    
    errors = []
    for path in config_paths:
        try:
            print(f"Trying to load configuration from {path}...")
            with open(path, 'r') as f:
                config = json.load(f)
            
            # Check if we have locations in the expected format
            if "locations" in config and "source" in config["locations"] and "destination" in config["locations"]:
                source = config["locations"]["source"]
                destination = config["locations"]["destination"]
                api_key = config.get("api_key")
                print(f"Successfully loaded configuration from {path} (locations format)")
                return source, destination, api_key
            
            # Check for direct source/destination format
            source = config.get("source")
            destination = config.get("destination")
            api_key = config.get("api_key")
            
            if not source or not destination:
                errors.append(f"Source or destination missing in {path}")
                continue
                
            print(f"Successfully loaded configuration from {path} (direct format)")
            return source, destination, api_key
        except (json.JSONDecodeError, FileNotFoundError) as e:
            errors.append(f"Error loading {path}: {str(e)}")
            continue
    
    # If we get here, none of the config files worked
    error_msg = "\n".join(errors)
    raise ValueError(f"Failed to load configuration from any file:\n{error_msg}")
    
if __name__ == "__main__":
    try:
        source, destination, config_api_key = load_locations_from_config()
        result = get_travel_time(source, destination, api_key=config_api_key)
        if result["success"]:
            print(f"Travel from {result['source']} to {result['destination']}:")
            print(f"Distance: {result['distance']}")
            print(f"Duration: {result['duration']}")

        else:
            print(f"Error: {result['error']}")
            print(f"Details: {result['details']}")

    except Exception as e:
        print(f"Error: {str(e)}")