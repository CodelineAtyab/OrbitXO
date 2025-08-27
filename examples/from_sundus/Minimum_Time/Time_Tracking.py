import requests
import datetime
import time
import json
import os


def load_dotenv():
    dotenv_path = ".env"
    if os.path.exists(dotenv_path):
        with open(dotenv_path) as f:
            for line in f:
                if line.strip() and not line.strip().startswith("#"):
                    key, sep, value = line.strip().partition("=")
                    if sep:
                        os.environ.setdefault(key, value)

load_dotenv()


SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")  
COOLDOWN_MINUTES = 30  
DATA_FILE = "min_times.json"  
print("SLACK_WEBHOOK_URL:", SLACK_WEBHOOK_URL)
# Example message for testing
message = "Notifier started successfully."
if SLACK_WEBHOOK_URL:
    resp = requests.post(SLACK_WEBHOOK_URL, json={"text": message})
    print(resp.status_code, resp.text)
else:
    print("[WARN] Slack webhook not configured")


def load_min_times():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_min_times(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

min_times = load_min_times()
last_alert_time = {}  


def send_slack_message(route, duration, prev_best):
    now = datetime.datetime.now()
    last_time = last_alert_time.get(route)

    
    if last_time and (now - last_time).total_seconds() < COOLDOWN_MINUTES * 60:
        print("[INFO] Cooldown active, skipping Slack notification")
        return

    if not SLACK_WEBHOOK_URL:
        print("[WARN] Slack webhook not configured")
        return

    time_saved = (prev_best - duration) if prev_best else 0
    message = (
        f"*🚨 NEW RECORD TRAVEL TIME! 🚨*\n"
        f"*🛣 Route:* {route}\n"
        f"*⏱ Current estimate:* {duration} min\n"
        f"*🏆 Previous best:* {prev_best if prev_best else 'N/A'} min\n"
        f"*💡 Time saved:* {time_saved} min\n"
        f"*📅 Recorded at:* {now.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json={"text": message})
        if resp.status_code == 200:
            print("[INFO] Slack notification sent ✅")
            last_alert_time[route] = now
        else:
            print(f"[ERROR] Slack send failed: {resp.text}")
    except Exception as e:
        print(f"[ERROR] Slack exception: {e}")


def record_travel_time(route, travel_time):
    prev_best = min_times.get(route)
    if prev_best is None or travel_time < prev_best:
        min_times[route] = travel_time
        save_min_times(min_times)
        print(f"[INFO] New minimum for {route}: {travel_time} min")
        send_slack_message(route, travel_time, prev_best)
    else:
        print(f"[INFO] No new minimum for {route}. Current: {travel_time} min, Best: {prev_best} min")


if __name__ == "__main__":
    while True:
        route = input("Enter route (e.g., Home->Work) or 'q' to quit: ")
        if route.lower() == "q":
            break
        try:
            travel_time = float(input("Enter travel time in minutes: "))
        except ValueError:
            print("[ERROR] Please enter a valid number")
            continue

        record_travel_time(route, travel_time)
        print("-" * 40)

