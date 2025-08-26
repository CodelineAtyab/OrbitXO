"""
Travel Time Minimum Tracker with Slack Notifications
Tracks and notifies when new minimum travel times are detected.
"""

import json
import os
import datetime
import time
import logging
import requests
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger("travel_time_monitor")

load_dotenv()


SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
NOTIFICATION_COOLDOWN = int(os.getenv("NOTIFICATION_COOLDOWN", "3600"))
DATA_FILE = "travel_times.json"

@dataclass
class TravelTimeRecord:
    """Data class representing a travel time record"""
    source: str
    destination: str
    duration: int
    timestamp: str
    
    @classmethod
    def create(cls, source: str, destination: str, duration: int, timestamp=None):
        """Factory method to create a new record"""
        if timestamp is None:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return cls(source, destination, duration, timestamp)

@dataclass
class MinimumTimeResult:
    """Data class for the result of a minimum time check"""
    is_new_minimum: bool
    route_key: str
    source: str
    destination: str
    current_duration: int
    previous_min: int
    time_saved: int
    current_time: str
    notification_sent: bool = False
    
    @property
    def new_minimum(self):
        return self.is_new_minimum
        
    def __getitem__(self, key):
        """Support dict-like access for backward compatibility"""
        attr_map = {
            "new_minimum": "is_new_minimum",
            "route_key": "route_key",
            "source": "source",
            "destination": "destination",
            "current_duration": "current_duration",
            "previous_min": "previous_min",
            "time_saved": "time_saved",
            "current_time": "current_time",
            "notification_sent": "notification_sent"
        }
        return getattr(self, attr_map.get(key, key))

class DataManager:
    """Handles data storage and retrieval"""
    
    def __init__(self, data_file: str):
        self.data_file = data_file
        
    def load(self) -> Dict:
        """Load data from file"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            logger.info(f"No existing data file found at {self.data_file}, creating new data store")
            return {}
    
    def save(self, data: Dict) -> None:
        """Save data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
        logger.debug(f"Data saved to {self.data_file}")


class NotificationManager:
    """Handles sending notifications"""
    
    def __init__(self):
        self.last_notification_time = {}
        
    def should_notify(self, route_key: str) -> bool:
        """Check if notification cooldown has elapsed"""
        current_time = time.time()
        if (route_key not in self.last_notification_time or
            current_time - self.last_notification_time[route_key] > NOTIFICATION_COOLDOWN):
            self.last_notification_time[route_key] = current_time
            return True
        return False
    
    def send_slack_notification(self, result: MinimumTimeResult) -> bool:
        """Send notification to Slack"""
        if not SLACK_WEBHOOK_URL:
            logger.warning("Slack webhook URL not configured. Skipping notification.")
            return False
            
        # Check cooldown period
        if not self.should_notify(result.route_key):
            logger.info("Notification cooldown active. Skipping notification.")
            return False
            
        slack_message = self._create_slack_message(result)
        
        try:
            logger.info("Sending Slack notification")
            logger.debug(f"Using webhook URL: {SLACK_WEBHOOK_URL[:35]}...")
            
            response = requests.post(
                SLACK_WEBHOOK_URL,
                json=slack_message,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            logger.debug(f"Slack API Response: {response.status_code} - {response.text}")
            
            if response.status_code != 200:
                logger.error(f"Slack API error: {response.status_code} - {response.text}")
                return False
                
            response.raise_for_status()
            logger.info("Notification sent successfully")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Slack notification: {str(e)}")
            return False
    
    def _create_slack_message(self, result: MinimumTimeResult) -> Dict:
        """Create formatted Slack message"""
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🚨 NEW RECORD TRAVEL TIME 🚨",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Route:* {result.source} → {result.destination}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Current estimate:* {result.current_duration} minutes"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Previous best:* {result.previous_min} minutes"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Time saved:* {result.time_saved} minutes"
                    }
                ]
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": f"Recorded at: {result.current_time}",
                        "emoji": True
                    }
                ]
            },
            {
                "type": "divider"
            }
        ]
        
        text_fallback = (
            f"🚨 NEW RECORD TRAVEL TIME 🚨\n"
            f"Route: {result.source} → {result.destination}\n"
            f"Current estimate: {result.current_duration} minutes\n"
            f"Previous best: {result.previous_min} minutes\n"
            f"Time saved: {result.time_saved} minutes\n"
            f"Recorded at: {result.current_time}"
        )
        
        return {
            "blocks": blocks,
            "text": text_fallback
        }


class MinimumTimeTracker:
    """Main class for tracking minimum travel times"""
    
    def __init__(self, data_file: str = DATA_FILE):
        self.data_manager = DataManager(data_file)
        self.notification_manager = NotificationManager()
        self.min_times = self.data_manager.load()
    
    def get_route_key(self, source: str, destination: str) -> str:
        """Generate unique key for a route"""
        return f"{source.lower().strip()}_{destination.lower().strip()}"
    
    def update_travel_time(self, source: str, destination: str, 
                          duration_minutes: int, current_time=None) -> MinimumTimeResult:
        """Update travel time and check for new minimum"""
        if current_time is None:
            current_time = datetime.datetime.now()
            
        time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        route_key = self.get_route_key(source, destination)
        
        new_min, previous_min, time_saved = self._process_time_record(
            route_key, source, destination, duration_minutes, time_str
        )
        
        self._update_history(route_key, duration_minutes, time_str)
        
        self.data_manager.save(self.min_times)
        
        return MinimumTimeResult(
            is_new_minimum=new_min,
            route_key=route_key,
            source=source,
            destination=destination,
            current_duration=duration_minutes,
            previous_min=previous_min,
            time_saved=time_saved,
            current_time=time_str
        )
    
    def _process_time_record(self, route_key: str, source: str, destination: str, 
                           duration: int, timestamp: str) -> Tuple[bool, int, int]:
        """Process a new time record and determine if it's a new minimum"""
        if route_key not in self.min_times:
            self.min_times[route_key] = {
                "source": source,
                "destination": destination,
                "min_duration": duration,
                "recorded_at": timestamp,
                "history": []
            }
            return True, duration, 0
        
        previous_min = self.min_times[route_key]["min_duration"]
        if duration < previous_min:
            time_saved = previous_min - duration
            self.min_times[route_key]["min_duration"] = duration
            self.min_times[route_key]["recorded_at"] = timestamp
            return True, previous_min, time_saved
        
        return False, previous_min, 0
    
    def _update_history(self, route_key: str, duration: int, timestamp: str) -> None:
        """Update route history"""
        if "history" not in self.min_times[route_key]:
            self.min_times[route_key]["history"] = []
        
        history_entry = {
            "duration": duration,
            "timestamp": timestamp
        }
        self.min_times[route_key]["history"].append(history_entry)
        
        self.min_times[route_key]["history"] = self.min_times[route_key]["history"][-10:]
    
    def send_slack_notification(self, result: MinimumTimeResult) -> bool:
        """Wrapper for backward compatibility"""
        return self.notification_manager.send_slack_notification(result)
    
    def should_send_notification(self, route_key: str) -> bool:
        """Wrapper for backward compatibility"""
        return self.notification_manager.should_notify(route_key)


def check_and_notify_new_minimum(source: str, destination: str, duration_minutes: int) -> MinimumTimeResult:
    """Convenience function to check travel time and notify if needed"""
    tracker = MinimumTimeTracker()
    result = tracker.update_travel_time(source, destination, duration_minutes)
    
    if result.is_new_minimum:
        print("[INFO] New minimum travel time detected!")
        notification_sent = tracker.send_slack_notification(result)
        result.notification_sent = notification_sent
    else:
        print("[INFO] Not a new minimum travel time")
        result.notification_sent = False
    
    return result


if __name__ == "__main__":
    # Example usage
    source = "Home"
    destination = "Work"
    duration_minutes = 22
    
    # Check travel time and notify if needed
    result = check_and_notify_new_minimum(source, destination, duration_minutes)
    
    if result.is_new_minimum:
        print(f"New minimum travel time: {result.current_duration} minutes")
        print(f"Previous minimum: {result.previous_min} minutes")
        print(f"Time saved: {result.time_saved} minutes")
        
        if result.notification_sent:
            print("Notification sent successfully")
        else:
            print("Notification was not sent (cooldown active or webhook not configured)")
    else:
        print(f"Not a new minimum. Current: {result.current_duration} minutes, " 
              f"Minimum: {result.previous_min} minutes")