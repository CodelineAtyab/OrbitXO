from api import load_address, get_travel_time
from database import store_travel_time
from notifier import send_slack_notification

def main():
    org, dest = load_address()
    time = get_travel_time(org, dest)
    store_travel_time(time)
    send_slack_notification(f"Travel time: {time}")

if __name__ == "__main__":
    main()
