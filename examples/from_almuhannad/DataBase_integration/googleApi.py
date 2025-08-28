import requests
import json
import os

def get_travel_time(source, destination, api_key=None):
    """
    Call Google Maps Routes API to get travel time between source and destination.
    
    Args:
        source (str): Source address or coordinates
        destination (str): Destination address or coordinates
        api_key (str, optional): Google Maps API key. If None, loads from config file.
        
    Returns:
        dict: Travel time information
    """
    # If API key is not provided, try to load it from config file
    if api_key is None:
        try:
            with open("config.json", 'r') as f:
                config = json.load(f)
                api_key = config.get("api_key")
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            # Fallback to environment variables if config file approach fails
            api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
        
        if not api_key:
            raise ValueError("Google Maps API key not found in config file or environment variables")
    
    # Using the newer Routes API (v2) instead of the legacy Distance Matrix API
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
        # Make API request
        print(f"Making API request to {base_url}")
        print(f"API key used: {api_key[:5]}...{api_key[-5:]}")  # Only show first and last 5 chars
        try:
            response = requests.post(base_url, headers=headers, json=data, timeout=5)
            print(f"Received response with status code: {response.status_code}")
            response.raise_for_status()  # Raise exception for HTTP errors
        except requests.exceptions.Timeout:
            print("API request timed out after 5 seconds")
            return {
                "success": False,
                "error": "Request timed out",
                "details": "The API request took too long to respond"
            }
        
        # Parse response
        result_data = response.json()
        
        # Check if routes exist
        if not result_data.get("routes"):
            return {
                "success": False,
                "error": "No routes found",
                "details": "The API could not find a route between the specified locations"
            }
        
        # Extract travel time information
        route = result_data["routes"][0]
        duration_seconds = int(route["duration"].rstrip("s"))
        distance_meters = route["distanceMeters"]
        
        # Convert duration to hours and minutes
        hours, remainder = divmod(duration_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if hours > 0:
            duration_text = f"{hours} hour{'s' if hours > 1 else ''}"
            if minutes > 0:
                duration_text += f" {minutes} min"
        else:
            duration_text = f"{minutes} min"
        
        # Convert distance to kilometers
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

# Example usage
if __name__ == "__main__":
    try:
        # Load locations from config file
        config_path = "config.json"
        source, destination = load_locations_from_config(config_path)
        
        # Get travel time
        result = get_travel_time(source, destination)
        
        if result["success"]:
            print(f"Travel from {result['source']} to {result['destination']}:")
            print(f"Distance: {result['distance']}")
            print(f"Duration: {result['duration']}")
        else:
            print(f"Error: {result['error']}")
            print(f"Details: {result['details']}")
            
    except Exception as e:
        print(f"Error: {str(e)}")