import requests
import json
import os
import datetime
import time
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
NOTIFICATION_COOLDOWN = 3600
DATA_FILE = "travel_times.json"

class MinimumTimeTracker:
    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.min_times = self._load_data()
        self.last_notification_time = {}

    def _load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.min_times, f, indent=2)

    def get_route_key(self, source, destination):
        return f"{source.lower().strip()}_{destination.lower().strip()}"

    def update_travel_time(self, source, destination, duration_minutes, current_time=None):
        if current_time is None:
            current_time = datetime.datetime.now()
        time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        route_key = self.get_route_key(source, destination)
        if route_key not in self.min_times:
            self.min_times[route_key] = {
                "source": source,
                "destination": destination,
                "min_duration": duration_minutes,
                "recorded_at": time_str,
                "history": []
            }
            new_min = True
            time_saved = 0
            previous_min = duration_minutes
        else:
            previous_min = self.min_times[route_key]["min_duration"]
            if duration_minutes < previous_min:
                new_min = True
                time_saved = previous_min - duration_minutes
                self.min_times[route_key]["min_duration"] = duration_minutes
                self.min_times[route_key]["recorded_at"] = time_str
            else:
                new_min = False
                time_saved = 0
        history_entry = {
            "duration": duration_minutes,
            "timestamp": time_str
        }
        if "history" not in self.min_times[route_key]:
            self.min_times[route_key]["history"] = []
        self.min_times[route_key]["history"].append(history_entry)
        self.min_times[route_key]["history"] = self.min_times[route_key]["history"][-10:]
        self._save_data()
        return {
            "new_minimum": new_min,
            "route_key": route_key,
            "source": source,
            "destination": destination,
            "current_duration": duration_minutes,
            "previous_min": previous_min,
            "time_saved": time_saved,
            "current_time": time_str
        }

    def should_send_notification(self, route_key):
        current_time = time.time()
        if (route_key not in self.last_notification_time or
            current_time - self.last_notification_time[route_key] > NOTIFICATION_COOLDOWN):
            self.last_notification_time[route_key] = current_time
            return True
        return False

    def send_slack_notification(self, update_info):
        if not SLACK_WEBHOOK_URL:
            print("[WARNING] Slack webhook URL not configured. Skipping notification.")
            return False
        if not self.should_send_notification(update_info["route_key"]):
            print("[INFO] Notification cooldown active. Skipping notification.")
            return False
        slack_message = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": ":rotating_light: NEW RECORD TRAVEL TIME :rotating_light:",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Route:* {update_info['source']} → {update_info['destination']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Current estimate:* {update_info['current_duration']} minutes"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Previous best:* {update_info['previous_min']} minutes"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Time saved:* {update_info['time_saved']} minutes"
                        }
                    ]
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "plain_text",
                            "text": f"Recorded at: {update_info['current_time']}",
                            "emoji": True
                        }
                    ]
                },
                {
                    "type": "divider"
                }
            ]
        }
        text_fallback = f":rotating_light: NEW RECORD TRAVEL TIME :rotating_light:\nRoute: {update_info['source']} → {update_info['destination']}\nCurrent estimate: {update_info['current_duration']} minutes\nPrevious best: {update_info['previous_min']} minutes\nTime saved: {update_info['time_saved']} minutes\nRecorded at: {update_info['current_time']}"
        slack_message["text"] = text_fallback
        try:
            print("[INFO] Sending Slack notification")
            print(f"[DEBUG] Using webhook URL: {SLACK_WEBHOOK_URL[:35]}...")
            response = requests.post(
                SLACK_WEBHOOK_URL,
                json=slack_message,
                headers={"Content-Type": "application/json"}
            )
            print(f"[DEBUG] Slack API Response Status: {response.status_code}")
            print(f"[DEBUG] Slack API Response Body: {response.text}")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Failed to send Slack notification: {str(e)}")
            return False

def check_and_notify_new_minimum(source, destination, duration_minutes):
    tracker = MinimumTimeTracker()
    update_result = tracker.update_travel_time(source, destination, duration_minutes)
    if update_result["new_minimum"]:
        print("[INFO] New minimum travel time detected!")
        notification_sent = tracker.send_slack_notification(update_result)
        update_result["notification_sent"] = notification_sent
    else:
        print("[INFO] Not a new minimum travel time")
        update_result["notification_sent"] = False
    return update_result

if __name__ == "__main__":
    source = "Home"
    destination = "Work"
    duration_minutes = 22
    result = check_and_notify_new_minimum(source, destination, duration_minutes)
    if result["new_minimum"]:
        print(f"New minimum travel time: {result['current_duration']} minutes")
        print(f"Previous minimum: {result['previous_min']} minutes")
        print(f"Time saved: {result['time_saved']} minutes")
        if result["notification_sent"]:
            print("Notification sent successfully")
        else:
            print("Notification was not sent (cooldown active or webhook not configured)")
    else:
        print(f"Not a new minimum. Current: {result['current_duration']} minutes, Minimum: {result['previous_min']} minutes")






