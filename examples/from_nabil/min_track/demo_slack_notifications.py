"""
Example of monitoring travel times and receiving Slack notifications
"""
import os
import sys
import time
from dotenv import load_dotenv

# Add script directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

# Import our modules
from minimum_time_tracking import check_and_notify_new_minimum

def main():
    """Demonstrate the minimum time tracking with notifications."""
    # Load environment variables
    load_dotenv()
    
    # Check if Slack webhook is configured
    slack_webhook = os.getenv("SLACK_WEBHOOK_URL")
    if not slack_webhook or slack_webhook == "YOUR_SLACK_WEBHOOK_URL":
        print("\n⚠️ WARNING: Slack webhook URL not configured in .env file")
        print("To receive notifications, you need to add your webhook URL.")
        print("Get a webhook URL from: https://api.slack.com/messaging/webhooks")
        print("\nContinuing with demo, but no notifications will be sent...\n")
    
    # Define example route
    source = "Home"
    destination = "Work"
    
    # Simulate several travel time checks with decreasing times
    times = [30, 28, 25, 26, 22, 24]
    
    print(f"\n🚗 Simulating travel time checks for route: {source} → {destination}")
    print("Each check will be made with a different travel time to simulate changing traffic conditions.\n")
    
    for i, duration in enumerate(times, 1):
        print(f"\n=== Check #{i} - Travel time: {duration} minutes ===")
        
        # Check if this is a new minimum and notify if needed
        result = check_and_notify_new_minimum(source, destination, duration)
        
        if result["new_minimum"]:
            print(f"✅ New minimum detected! {duration} minutes")
            print(f"Previous minimum: {result['previous_min']} minutes")
            print(f"Time saved: {result['time_saved']} minutes")
            
            if result["notification_sent"]:
                print("📬 Slack notification sent successfully!")
            else:
                print("❌ Slack notification not sent (webhook not configured or cooldown active)")
        else:
            print(f"ℹ️ Not a new minimum. Current: {duration} minutes")
            print(f"Existing minimum: {result['previous_min']} minutes")
        
        # Wait a bit between checks
        if i < len(times):
            print("\nWaiting 3 seconds before next check...")
            time.sleep(3)
    
    print("\n✅ Simulation complete!")
    print("Check your Slack channel to see if notifications were received.")
    print("\nTo run continuous monitoring with real-time data:")
    print("python travel_monitor.py monitor home work")

if __name__ == "__main__":
    main()
