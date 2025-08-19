from fastapi import FastAPI
import requests, os
from dotenv import load_dotenv
import uvicorn
load_dotenv()

app = FastAPI()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

LOCATIONS = {
    "home": "Muscat Grand Mall, Muscat, Oman",
    "work": "Codeline, Muscat, Oman"
}

@app.get("/travel-time")
def travel_time(source: str, destination: str):
    if not API_KEY:
        return {"error": "Missing API key."}
    
    if source not in LOCATIONS or destination not in LOCATIONS:
        return {"error": "Invalid source or destination."}
    
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.legs.duration,routes.legs.distanceMeters"
    }
    
    payload = {
        "origin": {
            "address": LOCATIONS[source]
        },
        "destination": {
            "address": LOCATIONS[destination]
        },
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
        "computeAlternativeRoutes": False
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        if "routes" not in data or len(data["routes"]) == 0:
            return {"error": "No routes found"}
        
        route = data["routes"][0]
        
        # Convert duration from seconds to readable format
        duration_seconds = int(route["duration"].rstrip('s'))
        duration_minutes = duration_seconds // 60
        duration_text = f"{duration_minutes} mins"
        
        # Convert distance from meters to kilometers
        distance_meters = route["distanceMeters"]
        distance_km = round(distance_meters / 1000, 1)
        distance_text = f"{distance_km} km"
        
        return {
            "from": LOCATIONS[source],
            "to": LOCATIONS[destination],
            "duration": duration_text,
            "distance": distance_text,
            "duration_seconds": duration_seconds,
            "distance_meters": distance_meters
        }
        
    except requests.exceptions.RequestException as e:
        return {"error": "Request failed", "message": str(e)}
    except KeyError as e:
        return {"error": "Unexpected response format", "missing_key": str(e)}
    except Exception as e:
        return {"error": "Unexpected error", "message": str(e)}

# Local run
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)