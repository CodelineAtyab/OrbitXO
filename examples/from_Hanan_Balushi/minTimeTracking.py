import time
import datetime
import requests
import json
import os 

SLACK = "https://hooks.slack.com/services/XXXX" #not real webhook bcz it requested me to upgrade slack
COOLDOWN = 3600  # 1 hour between alerts for same route
JSON_FILE = "min_travel_times.json"

# Load minimum travel times from JSON file if it exists
if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r") as f:
        # JSON keys are strings, convert them back to tuples
        min_travel_times = {tuple(k.split("->")): v for k, v in json.load(f).items()}
else:
    min_travel_times = {}

# Track last alert times in memory
last_alert_times = {}    



def save_minTravelTime():
    # Convert tuple keys to strings for JSON
    data = {f"{k[0]}->{k[1]}": v for k, v in min_travel_times.items()}
    with open(JSON_FILE, "w") as f:
        json.dump(data, f)

def slack_notification(route, current_time, prev_min, new_min):
    time_saved = prev_min - new_min
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = (
        f":rotating_light: *NEW RECORD TRAVEL TIME* :rotating_light:\n"
        f"*Route:* {route[0]} → {route[1]}\n"
        f"*Current estimate:* {new_min} minutes\n"
        f"*Previous best:* {prev_min} minutes\n"
        f"*Time saved:* {time_saved} minutes\n"
        f"*Recorded at:* _{now_str}_"
    )

    payload = {"text": message}
    response = requests.post(SLACK, json=payload)

    if response.status_code == 200:
        print("[INFO] Slack notification sent successfully")
    else:
        print(f"[ERROR] Failed to send Slack message: {response.status_code} {response.text}")



def min_travel_time(source, destination, travel_minutes):
    route = (source, destination)
    now = time.time()

    prev_min = min_travel_times.get(route, None)

    # If first time recording, just store
    if prev_min is None:
        min_travel_times[route] = travel_minutes
        save_minTravelTime()
        print(f"[INFO] New minimum travel time detected!")
        return

    # Check if new minimum
    if travel_minutes < prev_min:
        # Check cooldown
        last_alert = last_alert_times.get(route, 0)
        if now - last_alert > COOLDOWN:
            print("[INFO] New minimum travel time detected!")
            slack_notification(route, now, prev_min, travel_minutes)
            last_alert_times[route] = now

        # Update stored min
        min_travel_times[route] = travel_minutes
        save_minTravelTime()

if __name__ == "__main__":
    # Simulated travel times
    min_travel_time("Home", "Work", 25)  # First record
    min_travel_time("Home", "Work", 22)  # New Minimum 
    min_travel_time("Home", "Work", 21)  # Might be blocked by cooldown