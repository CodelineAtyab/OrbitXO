from fastapi import FastAPI, Query
import os
import requests
import dotenv
import json
from datetime import datetime
import schedule
import time
import threading
from pathlib import Path

# =========================
#   تحميل متغيرات البيئة
# =========================
dotenv.load_dotenv()
API_KEY = os.getenv("MAPS_API_KEY")
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")
COOLDOWN_SECONDS = int(os.getenv("ALERT_COOLDOWN_SECONDS", "900"))  # افتراضي 15 دقيقة

# =========================
#   إعدادات تطبيق FastAPI
# =========================
app = FastAPI(title="Travel Time Notifier")

# =========================
#   التخزين في ملف JSON
#   الهيكل:
#   {
#     "origin->destination": { "min": 25, "last_notified_ts": 1724500000 }
#   }
# =========================
DATA_FILE = Path("min_times.json")

def load_store() -> dict:
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_store(data: dict) -> None:
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

store = load_store()

def norm_key(origin: str, destination: str) -> str:
    # توحيد المفتاح لتجنب التكرار بسبب المسافات/الحروف
    return f"{origin.strip().lower()}->{destination.strip().lower()}"

# =========================
#   دوال مساعدة
# =========================
def send_slack_alert(message: str):
    """إرسال تنبيه إلى Slack باستخدام Webhook."""
    if not SLACK_WEBHOOK:
        print("[WARN] SLACK_WEBHOOK_URL غير مضبوط في .env")
        return

    try:
        resp = requests.post(SLACK_WEBHOOK, json={"text": message}, timeout=10)
        if resp.status_code == 200:
            print("[INFO] Slack notification sent")
        else:
            print(f"[ERROR] Slack send failed: {resp.status_code} | {resp.text}")
    except Exception as e:
        print(f"[ERROR] Slack exception: {e}")

def get_google_travel(origin: str, destination: str):
    """استعلام Google Routes API وإرجاع (الدقائق، الكيلومترات) أو خطأ."""
    if not API_KEY:
        return None, None, "MAPS_API_KEY مفقود في .env"

    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters"
    }
    body = {
        "origin": {"address": origin},
        "destination": {"address": destination},
        "travelMode": "DRIVE"
    }

    try:
        r = requests.post(url, headers=headers, json=body, timeout=15)
        data = r.json()
    except requests.Timeout:
        return None, None, "Google API timeout"
    except Exception as e:
        return None, None, f"Google API error: {e}"

    if "routes" not in data:
        return None, None, data.get("error", {}).get("message", "Unknown error from Google")

    route = data["routes"][0]
    # route["duration"] مثل "2700s"
    duration_iso = route.get("duration", "0s")
    try:
        seconds = int(duration_iso.replace("s", ""))
    except Exception:
        seconds = 0
    minutes = max(round(seconds / 60), 0)

    distance_m = route.get("distanceMeters", 0)
    distance_km = round(distance_m / 1000, 2)

    return minutes, distance_km, None

def check_route(origin: str, destination: str):
    """تفقد زمن المسار وتحديث الرقم القياسي عند تحقق شرط رقم قياسي جديد + تبريد."""
    current_minutes, distance_km, err = get_google_travel(origin, destination)
    if err:
        return {"error": err}

    key = norm_key(origin, destination)
    record = store.get(key, {"min": None, "last_notified_ts": 0})
    prev_best = record.get("min")
    last_ts = int(record.get("last_notified_ts", 0))

    new_record = False
    slack_status = None

    # فقط نحدّث إذا الزمن الحالي أقل من المينيمم المسجّل
    if prev_best is None or current_minutes < prev_best:
        new_record = True
        # تحديث أقل زمن دائمًا لأنه رقم قياسي جديد
        record["min"] = current_minutes

        # منع الإزعاج: تبريد
        now_ts = int(time.time())
        cooldown_ok = (now_ts - last_ts) >= COOLDOWN_SECONDS

        if cooldown_ok:
            saved = (prev_best - current_minutes) if prev_best is not None else 0
            msg = (
                "🚨 *NEW RECORD TRAVEL TIME* 🚨\n"
                f"*Route:* {origin.strip()} → {destination.strip()}\n"
                f"*Current estimate:* {current_minutes} minutes\n"
                f"*Previous best:* {prev_best if prev_best is not None else 'N/A'} minutes\n"
                f"*Time saved:* {saved} minutes\n"
                f"*Recorded at:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            send_slack_alert(msg)
            record["last_notified_ts"] = now_ts
            slack_status = {"sent": True, "cooldown": COOLDOWN_SECONDS}
        else:
            slack_status = {"sent": False, "reason": "cooldown_active", "cooldown": COOLDOWN_SECONDS}

        # حفظ السجل
        store[key] = record
        save_store(store)

    # لو الزمن مساوي أو أسوأ: لا نغيّر المينيمم ولا نرسل Slack
    return {
        "route": f"{origin.strip()} → {destination.strip()}",
        "current_minutes": current_minutes,
        "distance_km": distance_km,
        "previous_min_minutes": prev_best,
        "new_record": new_record,
        "cooldown_seconds": COOLDOWN_SECONDS,
        "slack": slack_status
    }

# =========================
#   Endpoints
# =========================
@app.get("/travel-time")
def travel_time(origin: str = Query(...), destination: str = Query(...)):
    """Endpoint يدوي: يرجّع الزمن الحالي + يحدّث الرقم القياسي + (Slack مع تبريد)."""
    return check_route(origin, destination)

@app.get("/records")
def list_records():
    """عرض كل الأرقام القياسية المخزّنة."""
    rows = []
    for k, v in store.items():
        o, d = k.split("->", 1)
        rows.append({
            "origin": o,
            "destination": d,
            "min_minutes": v.get("min"),
            "last_notified_ts": v.get("last_notified_ts")
        })
    return rows

# =========================
#   Scheduler (تجريبي)
#   يفحص تلقائياً كل 10 دقائق
#   ملاحظة: للإنتاج استخدم Cron/خدمة مجدول خارجية
# =========================
def auto_check():
    routes = [
        ("Muscat", "Nizwa"),
        ("Home", "Work"),
    ]
    for origin, destination in routes:
        print(f"[AUTO] Checking {origin} -> {destination}")
        try:
            # بإمكانك مناداة الدالة مباشرة بدل GET، لكن نستخدم GET لتوحيد المنطق
            requests.get(
                "http://127.0.0.1:8000/travel-time",
                params={"origin": origin, "destination": destination},
                timeout=10
            )
        except Exception as e:
            print(f"[AUTO] request error: {e}")

def run_scheduler():
    schedule.every(10).minutes.do(auto_check)
    while True:
        schedule.run_pending()
        time.sleep(1)

# تشغيل الجدولة في الخلفية (مناسب للتجارب على single worker)
threading.Thread(target=run_scheduler, daemon=True).start()