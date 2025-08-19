
from fastapi import FastAPI, Query
import os
import requests
import dotenv
dotenv.load_dotenv()
api_key = os.getenv("MAPS_API_KEY")
app = FastAPI()
@app.get("/travel-time")
def get_travel_time(origin: str = Query(...), destination: str = Query(...)):
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters"
    }
    body = {
        "origin": { "address": origin },
        "destination": { "address": destination },
        "travelMode": "DRIVE"
    }
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    if "routes" not in data:
        return {"error": data.get("error", {}).get("message", "Unknown error")}
    route = data["routes"][0]
    return {
        "origin": origin,
        "destination": destination,
        "duration": route["duration"],
        "distance_km": route["distanceMeters"] / 1000
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Google_Maps_API:app", host="127.0.0.1", port=8000, reload=True)