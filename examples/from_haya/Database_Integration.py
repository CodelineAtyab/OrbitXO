import os
from dotenv import load_dotenv
import requests
import logging
import time
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from apscheduler.schedulers.background import BackgroundScheduler

# ================== Load environment variables ==================
load_dotenv()
API_KEY = os.getenv("MAPS_API_KEY")
if not API_KEY:
    raise ValueError("❌ MAPS_API_KEY not set in .env file!")

# ================== Logging ==================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(filename)s] %(message)s"
)

# ================== Database (SQLite) ==================
DATABASE_URL = "sqlite:///google_map_api.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class TravelTime(Base):
    __tablename__ = "travel_times"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    origin = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    duration_minutes = Column(Integer, nullable=False)

Base.metadata.create_all(engine)

# ================== Google Maps API ==================
def fetch_travel_duration(origin: str, destination: str):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {"origin": origin, "destination": destination, "key": API_KEY}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data["status"] != "OK":
            logging.error(f"Google API error: {data['status']}")
            print("❌ API error:", data)
            return None
        duration_seconds = data["routes"][0]["legs"][0]["duration"]["value"]
        print(f"✅ Got duration {duration_seconds//60} mins for {origin} -> {destination}")
        return duration_seconds
    except Exception as e:
        logging.error(f"Exception in fetch_travel_duration: {e}")
        return None

# ================== Save to DB ==================
def save_travel_time(origin: str, destination: str, duration_seconds: int):
    session = SessionLocal()
    try:
        if duration_seconds is None:
            print("⚠️ No duration, skipping save.")
            return
        record = TravelTime(
            timestamp=datetime.now(),
            origin=origin,
            destination=destination,
            duration_minutes=duration_seconds // 60
        )
        session.add(record)
        session.commit()
        print(f"💾 Saved to DB: {record.origin} -> {record.destination} = {record.duration_minutes} mins")
    except Exception as e:
        logging.error(f"Failed to save: {e}")
        session.rollback()
    finally:
        session.close()

# ================== Scheduled Job ==================
def scheduled_job(origin, destination):
    duration_seconds = fetch_travel_duration(origin, destination)
    save_travel_time(origin, destination, duration_seconds)

# ================== Retrieve Historical Data ==================
def get_historical_data(origin: str, destination: str, date: str):
    session = SessionLocal()
    results = session.query(TravelTime).filter(
        TravelTime.origin == origin,
        TravelTime.destination == destination,
        TravelTime.timestamp.like(f"{date}%")
    ).all()
    session.close()
    if not results:
        print(f"❌ No records found for {origin} -> {destination} on {date}")
        return
    print(f"📅 Records for {date}:")
    for r in results:
        print(f"{r.timestamp.strftime('%H:%M:%S')} - {r.duration_minutes} mins")

# ================== Main ==================
if __name__ == "__main__":
    # ===== Request origin and destination =====
    origin = input("Enter origin: ").strip()
    destination = input("Enter destination: ").strip()
    if not origin or not destination:
        raise ValueError("❌ Origin and destination cannot be empty")

    # ===== Run immediately for testing =====
    scheduled_job(origin, destination)

    # ===== Run periodically every 15 minutes =====
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: scheduled_job(origin, destination), "interval", minutes=15)
    scheduler.start()
    logging.info("Scheduler started. Recording every 15 minutes...")

    try:
        while True:
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logging.info("Scheduler stopped.")


from Database_Integration import get_historical_data
get_historical_data("muscat", "fnja", "2025-08-26")