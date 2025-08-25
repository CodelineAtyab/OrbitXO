import requests
import json
import os
from dotenv import load_dotenv
from api_logger import log_api_call, log_error

# Load API key from environment variable
load_dotenv()

def get_distance_matrix(origins, destinations, api_key=None, mode="DRIVE", units="metric"):
    """
    Call the Google Maps Routes API to get distance and duration between origins and destinations.
    
    Args:
        origins (list or str): List of origin addresses or coordinates, or a single origin as a string
        destinations (list or str): List of destination addresses or coordinates, or a single destination as a string
        api_key (str, optional): Google Maps API key. If None, will try to load from environment variable GOOGLE_MAPS_API_KEY
        mode (str, optional): Mode of transportation. Options: "DRIVE", "WALK", "BICYCLE", "TRANSIT". Default is "DRIVE"
        units (str, optional): Unit system (metric or imperial). Default is "metric"
        
    Returns:
        dict: JSON response from the Routes API, formatted to be similar to the legacy Distance Matrix API
    """
    # Get API key from environment if not provided
    if api_key is None:
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not api_key:
            raise ValueError("API key not provided and GOOGLE_MAPS_API_KEY not found in environment")
    
    # Base URL for the Routes API
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    
    # Ensure origins and destinations are lists
    if isinstance(origins, str):
        origins = [origins]
    if isinstance(destinations, str):
        destinations = [destinations]
    
    # Map the legacy mode values to Routes API travel modes
    travel_mode_map = {
        "driving": "DRIVE",
        "walking": "WALK",
        "bicycling": "BICYCLE",
        "transit": "TRANSIT"
    }
    
    # Convert legacy mode to Routes API mode if needed
    if mode.lower() in travel_mode_map:
        mode = travel_mode_map[mode.lower()]
    
    # The Routes API uses a different structure than the Matrix API
    # We need to create one request for each origin-destination pair
    all_routes = []
    all_responses = []
    
    # For each origin-destination pair
    for origin in origins:
        for destination in destinations:
            # Build the request body for this pair
            request_body = {
                "origin": {
                    "address": origin
                },
                "destination": {
                    "address": destination
                },
                "travelMode": mode,
                "routingPreference": "TRAFFIC_AWARE",
                "computeAlternativeRoutes": False,
                "languageCode": "en-US",
                "units": "METRIC" if units.lower() == "metric" else "IMPERIAL"
            }
    
            # Set headers for the API request
            headers = {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": api_key,
                "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline"
            }
            
            # Make the API request
            try:
                response = requests.post(url, json=request_body, headers=headers)
                
                # Store origin, destination, and response for later processing
                all_responses.append({
                    "origin": origin,
                    "destination": destination,
                    "response": response
                })
                
                # Log the API call
                try:
                    response_data = response.json() if response.status_code == 200 else None
                    log_api_call(
                        origin=origin,
                        destination=destination,
                        mode=mode,
                        api_key_used=api_key is not None,
                        response_status=response.status_code,
                        response_data=response_data
                    )
                except Exception as log_err:
                    print(f"Error logging API call: {str(log_err)}")
                
                # Print debug info for first request only
                if len(all_responses) == 1:
                    print(f"Sample response status code: {response.status_code}")
                    print(f"Sample response headers: {response.headers}")
                    print(f"Sample response content: {response.text[:1000]}...")
                
            except Exception as e:
                log_error("distance_matrix", "get_distance_matrix", f"Error requesting route from {origin} to {destination}: {str(e)}")
                print(f"Error requesting route from {origin} to {destination}: {str(e)}")
    
    # Create a formatted response similar to the Distance Matrix API format
    formatted_response = {
        "origin_addresses": origins,
        "destination_addresses": destinations,
        "rows": [],
        "status": "OK"
    }
    
    # We need to organize the responses by origin
    origin_to_elements = {}
    
    # Process all responses
    for resp_data in all_responses:
        origin = resp_data["origin"]
        destination = resp_data["destination"]
        response = resp_data["response"]
        
        # Create elements list for this origin if it doesn't exist yet
        if origin not in origin_to_elements:
            origin_to_elements[origin] = []
        
        # Process the response for this origin-destination pair
        if response.status_code == 200:
            try:
                data = response.json()
                
                if "routes" in data and data["routes"]:
                    route = data["routes"][0]  # Get the first route
                    distance_meters = route.get("distanceMeters", 0)
                    
                    # Extract duration in seconds from string like "1234s"
                    duration_str = route.get("duration", "0s")
                    duration_seconds = int(duration_str.rstrip("s")) if duration_str.endswith("s") else 0
                    
                    # Format the text representations
                    distance_text = f"{round(distance_meters/1000, 1)} km" if units.lower() == "metric" else f"{round(distance_meters/1609.34, 1)} mi"
                    
                    hours, remainder = divmod(duration_seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    
                    if hours > 0:
                        duration_text = f"{hours} hour{'s' if hours != 1 else ''} {minutes} min"
                    else:
                        duration_text = f"{minutes} min"
                    
                    element_data = {
                        "status": "OK",
                        "distance": {
                            "value": distance_meters,
                            "text": distance_text
                        },
                        "duration": {
                            "value": duration_seconds,
                            "text": duration_text
                        }
                    }
                else:
                    element_data = {"status": "ZERO_RESULTS"}
            except Exception as e:
                print(f"Error processing response for {origin} to {destination}: {str(e)}")
                element_data = {"status": "UNKNOWN_ERROR"}
        else:
            try:
                error_data = response.json()
                error_message = "Unknown error"
                if "error" in error_data:
                    error_message = error_data["error"].get("message", error_message)
                element_data = {"status": "REQUEST_DENIED", "error_message": error_message}
            except:
                element_data = {"status": "REQUEST_DENIED", "error_message": f"HTTP {response.status_code}"}
        
        # Add this element to the current origin's elements
        origin_to_elements[origin].append(element_data)
        
    # Now convert the organized data to rows in the formatted response
    for origin in origins:
        if origin in origin_to_elements:
            formatted_response["rows"].append({"elements": origin_to_elements[origin]})
        else:
            # If we have no data for this origin, add empty elements
            empty_elements = []
            for _ in destinations:
                empty_elements.append({"status": "UNKNOWN_ERROR"})
            formatted_response["rows"].append({"elements": empty_elements})
    
    # Check for any successful responses
    has_success = False
    for row in formatted_response["rows"]:
        for element in row["elements"]:
            if element["status"] == "OK":
                has_success = True
                break
        if has_success:
            break
    
    # Set overall status
    if not has_success:
        formatted_response["status"] = "ZERO_RESULTS"
        
        # Look for error messages
        error_messages = []
        for row in formatted_response["rows"]:
            for element in row["elements"]:
                if "error_message" in element:
                    error_messages.append(element["error_message"])
        
        # Add the first error message as the overall error message
        if error_messages:
            formatted_response["error_message"] = error_messages[0]
    
    return formatted_response

if __name__ == "__main__":
    # Example usage
    API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
    
    origins = ["Seattle, WA"]
    destinations = ["San Francisco, CA", "Portland, OR"]
    
    result = get_distance_matrix(origins, destinations, API_KEY)
    
    # Pretty print the result
    print(json.dumps(result, indent=2))
    
    # Print a more human-readable summary
    if result.get("status") == "OK":
        for i, origin in enumerate(result["origin_addresses"]):
            print(f"\nFrom: {origin}")
            for j, destination in enumerate(result["destination_addresses"]):
                element = result["rows"][i]["elements"][j]
                if element["status"] == "OK":
                    print(f"  To: {destination}")
                    print(f"    Distance: {element['distance']['text']}")
                    print(f"    Duration: {element['duration']['text']}")
                else:
                    print(f"  To: {destination} - {element['status']}")
    else:
        print(f"\nError: {result.get('error_message', 'Unknown error')}")