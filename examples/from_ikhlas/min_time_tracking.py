import requests
import datetime
import dotenv
import os
import json

#Google/Slack API
dotenv.load_dotenv()
GOOGLE_API_KEY=os.getenv("GOOGLE_MAPS_API_KEY")
slack_webhook_url=os.getenv("SLACK_WEBHOOK_URL")

#tracking
min_time={}
cooldown_time=30
last_alert_time={}

#slack alert
def slack_alert(route,previous_duration,new_duration):
    now_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #handle none case 
    time_saved = previous_duration-new_duration if previous_duration is not None else 0
    prev_display = previous_duration if previous_duration is not None else "N/A"

    message={
        "text": (
            "🚨 *NEW RECORD TRAVEL TIME* 🚨\n"
            f"*Route:* {route}\n"
            f"*Current estimate:* {new_duration} minutes\n"
            f"*Previous best:* {prev_display} minutes\n"
            f"*Time saved:* {time_saved} minutes\n"
            f"*Recorded at:* {now_time}"
        )
    }
    requests.post(slack_webhook_url, json=message)
    print("[INFO] Sending Slack notification")

#track travel time
def travel_time(route,new_duration):
    now_time=datetime.datetime.now()
    previous_duration=min_time.get(route)
    last_alert=last_alert_time.get(route)
    
    if previous_duration is None or new_duration < previous_duration:
        min_time[route]=new_duration
        print("[INFO] New minimum travel time detected!")

        #to check the cooldown
        if not last_alert or (now_time-last_alert).seconds>cooldown_time*60:
            slack_alert(route,previous_duration,new_duration)
            last_alert_time[route]=now_time
        else:
            print("[INFO] Within cooldown window, no Slack alert.")
    else:
        print("[INFO] Not a new minimum.")

#Google API call 
def fetch_travel_time(origin,destination):
    url="https://routes.googleapis.com/directions/v2:computeRoutes"
    headers={"content-type":"application/json",
             "X-Goog-Api-Key":GOOGLE_API_KEY,
             "X-Goog-FieldMask":"routes.duration,routes.distanceMeters"}
    
    body = {"origin": {"address": origin},
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
    response=requests.post(url,headers=headers,data=json.dumps(body))
    if response.ok:
        data=response.json()
        route=data["routes"][0]
        duration_seconds=int(route["duration"].replace("s",""))
        duration_minutes=duration_seconds/60
        distance_km=route["distanceMeters"]/1000

        print(f"Google API: {duration_minutes:.1f} min, {distance_km:.2f} km")
        return duration_minutes
    else:
        print("Error:", response.status_code)
        print(response.text)
        return None


if __name__ == "__main__":
    origin="Muscat Private Hospital, Muscat, Oman"
    destination="Codeline, Muscat, Oman"
    route_name="Home → Work"

    duration=fetch_travel_time(origin, destination)
    if duration:
        travel_time(route_name, duration)