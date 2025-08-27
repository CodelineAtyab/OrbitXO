import requests
import json
import configparser
import dotenv
import os
from logging_config import log_setup

log = log_setup("api")

def load_address(config_file="application.config"):
    log.info("Starting Parameters (Source,Destination) Request")
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
        org = config.get("Locations", "home")
        dest = config.get("Locations", "work")
        log.debug(f"Recieved parameters: {{source: \"{org}\", destination: \"{dest}\"}}")
        return org,dest
    except Exception as e:
        print(f"Config error: {e}")
        exit()

def get_travel_time(org, dest):
    log.info("Starting API request to Google Maps")
    dotenv.load_dotenv()
    API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
    URL = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={org}&destinations={dest}&key={API_KEY}"

    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON from the API response.")
        return

    if data.get('status') == "OK":
        try:
            row = data['rows'][0]['elements'][0]
            if row['status'] == "OK":
                distance = row["distance"]["text"]
                duration = row["duration"]["text"]
                print(f"Source: {org}")
                print(f"Destination: {dest}")
                print(f"Estimated Travel Time: {duration}") 
                print(f"Distance: {distance}")
                log.info(f"Received response: {row['status']} OK")
                return duration
            else:
                print(f"Element error: {row.get('status')}")
        except (IndexError, KeyError) as e:
            print(f"Error extracting data: {e}")
    else:
        print(f"API error: {data.get('status')} - {data.get('error_message', 'No error message provided')}")
    


