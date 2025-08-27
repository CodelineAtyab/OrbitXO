import requests
import json
import os
import dotenv

#get API key from .env file
dotenv.load_dotenv()
API_KEY=os.getenv("GOOGLE_MAPS_API_KEY")
url="https://routes.googleapis.com/directions/v2:computeRoutes"

headers={
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"
}

#request body
body={
    "origin": {
        "address":"Muscat Private Hospital, Muscat, Oman"
    },
    "destination": {
        "address":"Codeline, Muscat, Oman"
    },
    "travelMode":"DRIVE",
    "routingPreference":"TRAFFIC_AWARE",
    "computeAlternativeRoutes":False,
    "routeModifiers": {
        "avoidTolls":False,
        "avoidHighways":False,
        "avoidFerries":False
    },
    "languageCode":"en-US",
    "units":"METRIC"
}

#post request
response=requests.post(url, headers=headers, data=json.dumps(body))

#response handle
if response.ok:
    data=response.json()
    route=data["routes"][0]
    duration_seconds=int(route["duration"].rstrip("s"))
    duration_minutes=duration_seconds /60 #in min
    distance_km=route["distanceMeters"] /1000 #in km

    print("The estimated travel time: {:.1f}minutes".format(duration_minutes))
    print("Distance: {:.2f}km".format(distance_km))
else:
    print("Error:", response.status_code)
    print(response.text)
