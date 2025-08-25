import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

def send_slack_notification(route_data, slack_url=None):
    """
    Send a notification to Slack with route information.
    
    Args:
        route_data (dict): Dictionary containing route information
        slack_url (str, optional): Slack webhook URL. If None, it will be loaded from env var
        
    Returns:
        bool: True if notification was sent successfully, False otherwise
    """
    # Get Slack webhook URL from environment if not provided
    if slack_url is None:
        slack_url = os.getenv("SLACK_URL")
        if not slack_url:
            print("Error: SLACK_URL not found in environment variables")
            return False
    
    # Format the message
    message = format_slack_message(route_data)
    
    # Send the notification
    try:
        response = requests.post(
            slack_url,
            json=message,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print(f"Notification sent to Slack successfully")
            return True
        else:
            print(f"Failed to send notification to Slack. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error sending notification to Slack: {str(e)}")
        return False

def format_slack_message(route_data):
    """
    Format route data into a Slack message.
    
    Args:
        route_data (dict): Dictionary containing route information
        
    Returns:
        dict: Formatted Slack message payload
    """
    # Get current time if not in route_data
    timestamp = route_data.get('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Format the message
    message_text = f"*Route Update: {route_data.get('origin', 'N/A')} to {route_data.get('destination', 'N/A')}*"
    
    # Create color based on whether this is a minimum time/distance
    color = "#36a64f"  # Default green
    if route_data.get('is_min_distance') or route_data.get('is_min_duration'):
        color = "#FF9900"  # Orange for new minimum
    
    # Build notification fields
    fields = [
        {
            "title": "Time",
            "value": timestamp,
            "short": True
        },
        {
            "title": "From",
            "value": route_data.get('origin', 'N/A'),
            "short": True
        },
        {
            "title": "To",
            "value": route_data.get('destination', 'N/A'),
            "short": True
        },
        {
            "title": "Distance",
            "value": route_data.get('distance_text', 'N/A'),
            "short": True
        },
        {
            "title": "Duration",
            "value": route_data.get('duration_text', 'N/A'),
            "short": True
        }
    ]
    
    # Add minimum indicators if applicable
    if route_data.get('is_min_distance'):
        fields.append({
            "title": "🏆 New Record",
            "value": "Shortest distance so far!",
            "short": False
        })
    
    if route_data.get('is_min_duration'):
        fields.append({
            "title": "⚡ New Record",
            "value": "Fastest route so far!",
            "short": False
        })
    
    # Build the complete message
    message = {
        "text": message_text,
        "attachments": [
            {
                "color": color,
                "fields": fields,
                "footer": "Google Maps Route Tracker",
                "ts": int(datetime.now().timestamp())
            }
        ]
    }
    
    return message

# If this script is run directly, test sending a notification
if __name__ == "__main__":
    print("Slack Route Notification - Test")
    print("===============================")
    
    # Create a sample route_data
    test_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "origin": "Seattle, WA",
        "destination": "Portland, OR",
        "distance_meters": 280179,
        "distance_text": "280.2 km",
        "duration_seconds": 9945,
        "duration_text": "2 hours 45 min",
        "is_min_distance": True,
        "is_min_duration": False
    }
    
    # Send a test notification
    send_slack_notification(test_data)
