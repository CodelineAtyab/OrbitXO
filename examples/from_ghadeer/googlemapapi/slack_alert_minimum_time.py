from fastapi import FastAPI, Query
import os
import requests
import dotenv
import json
from datetime import datetime

dotenv.load_dotenv()
api_key = os.getenv("MAPS_API_KEY")
slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

app = FastAPI()

# ملف لتخزين البيانات
DATA_FILE = "min_times.json"

# تحميل البيانات السابقة عند تشغيل البرنامج
def load_min_times():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# حفظ البيانات في الملف
def save_min_times(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# القراءات المحفوظة
min_times = load_min_times()


@app.get("/travel-time")
def get_travel_time(origin: str = Query(...), destination: str = Query(...)):
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters"
    }

    body = {
        "origin": {"address": origin},
        "destination": {"address": destination},
        "travelMode": "DRIVE"
    }

    response = requests.post(url, headers=headers, json=body)
    data = response.json()

    if "routes" not in data:
        return {"error": data.get("error", {}).get("message", "Unknown error")}

    route = data["routes"][0]
    duration = route["duration"]  # ex: "2700s"
    distance_km = route["distanceMeters"] / 1000

    # تحويل الوقت للـ دقائق
    duration_minutes = int(duration.replace("s", "")) // 60

    # المفتاح (المسار origin->destination)
    key = f"{origin}->{destination}"
    prev_best = min_times.get(key)

    new_record = False
    alert_msg = None

    if prev_best is None or duration_minutes < prev_best:
        min_times[key] = duration_minutes
        save_min_times(min_times)  # تحديث الملف
        new_record = True
        alert_msg = (
            f"🚨 NEW RECORD TRAVEL TIME 🚨\n"
            f"Route: {origin} → {destination}\n"
            f"Current estimate: {duration_minutes} minutes\n"
            f"Previous best: {prev_best if prev_best else 'N/A'} minutes\n"
            f"Time saved: {(prev_best - duration_minutes) if prev_best else 0} minutes\n"
            f"Recorded at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        send_slack_alert(alert_msg)

    return {
        "origin": origin,
        "destination": destination,
        "duration_minutes": duration_minutes,
        "distance_km": distance_km,
        "new_record": new_record
    }


def send_slack_alert(message: str):
    """إرسال رسالة إلى Slack"""
    if not slack_webhook:
        print("[WARN] Slack webhook not configured")
        return

    try:
        resp = requests.post(slack_webhook, json={"text": message})
        if resp.status_code == 200:
            print("[INFO] Slack notification sent")
        else:
            print(f"[ERROR] Slack send failed: {resp.text}")
    except Exception as e:
        print(f"[ERROR] Slack exception: {e}")