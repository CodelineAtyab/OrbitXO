import requests
import json
import os
import dotenv
import sqlite3
from datetime import datetime

#loading API key
dotenv.load_dotenv()
API_KEY=os.getenv("GOOGLE_MAPS_API_KEY")

DB_FILE="traffic.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def fetch_travel_time(source,destination):
    "Call Google Maps Routes API to get travel time and distance"
    url="https://routes.googleapis.com/directions/v2:computeRoutes"

    headers={
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters"
    }

    body={
        "origin": {"address": source},
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
        duration_seconds=int(route["duration"].rstrip("s"))
        duration_minutes=duration_seconds/60
        distance_km=route["distanceMeters"]/1000
        return duration_minutes, distance_km
    else:
        print("[ERROR] Google API:", response.status_code, response.text)
        return None, None

def record_travel_time(source,destination):
    "Fetch travel time and store into SQLite database"
    minutes,distance=fetch_travel_time(source, destination)
    if minutes is None:
        return

    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO travel_times (timestamp,source,destination,duration_minutes,distance_km) VALUES (?, ?, ?, ?, ?)",
        (timestamp, source, destination, minutes, distance)
    )
    conn.commit()
    conn.close()

    print(f"[INFO] Recorded travel time: {minutes:.1f} minutes ({source} -> {destination}) at {timestamp}")

def get_historical_data(source, destination, date):
    """Retrieve all records for a given date"""
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        "SELECT timestamp, duration_minutes FROM travel_times WHERE source=? AND destination=? AND date(timestamp)=?",
        (source, destination, date)
    )
    rows=cursor.fetchall()
    conn.close()

    print(f"Date: {date}")
    for row in rows:
        time=row[0].split(" ")[1]  # HH:MM:SS
        print(f"{time} - {row[1]:.1f} minutes")
