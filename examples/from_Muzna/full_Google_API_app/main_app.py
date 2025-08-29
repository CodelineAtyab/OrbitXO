import os
import json
import logging
from datetime import datetime, timedelta, date
from typing import List, Dict, Union, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse  # Correct import for FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn
import httpx

# New Imports for Database and Scheduling
from sqlalchemy import create_engine, Column, Integer, String, DateTime, text
from sqlalchemy.orm import declarative_base, sessionmaker
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.exc import SQLAlchemyError

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
app = FastAPI(title="Live Travel Time & Route Manager")

# Mount the 'ui' directory to serve static files (like index.html)
app.mount("/static", StaticFiles(directory="ui"), name="static")

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
NOTIFICATION_COOLDOWN_MINUTES = 60
CONFIG_FILE = "routes.json"

# --- Database Configuration (replacing TinyDB) ---
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = "db"
DB_PORT = "3306"
DB_NAME = os.getenv("MYSQL_DATABASE")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    logging.error(f"Failed to create database engine: {e}")
    engine = None
    SessionLocal = None


# Define the database models
class TravelRecord(Base):
    __tablename__ = "travel_records"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(255), index=True)
    destination = Column(String(255), index=True)
    duration_seconds = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

class BestTravelTime(Base):
    __tablename__ = "best_travel_times"
    id = Column(Integer, primary_key=True, index=True)
    route_key = Column(String(512), unique=True, index=True)
    source = Column(String(255))
    destination = Column(String(255))
    duration_seconds = Column(Integer)
    last_updated = Column(DateTime, default=datetime.utcnow)

def create_tables():
    """Creates database tables if they do not exist."""
    if engine:
        logging.info("Attempting to create database tables...")
        try:
            Base.metadata.create_all(bind=engine)
            logging.info("Database tables created or already exist.")
        except SQLAlchemyError as e:
            logging.error(f"Error creating database tables: {e}")
    else:
        logging.error("Database engine is not initialized. Cannot create tables.")


# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
class TravelRequest(BaseModel):
    source_address: str
    destination_address: str

class RouteEntry(BaseModel):
    name: str
    source_address: str
    destination_address: str

class AddRouteRequest(BaseModel):
    route_name: str
    source_address: str
    destination_address: str

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- Helper Functions for Route Management ---
def load_routes():
    """Loads existing routes from the configuration file."""
    if not os.path.exists(CONFIG_FILE):
        return []
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        logging.error(f"Failed to load routes from {CONFIG_FILE}: {e}")
        return []

def save_routes(routes: List[Dict]):
    """Saves the current list of routes to the configuration file."""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(routes, f, indent=4)
    except IOError as e:
        logging.error(f"Failed to save routes to {CONFIG_FILE}: {e}")

# --- Core Functions for Travel Time & Notifications ---
async def send_slack_notification(source_address: str, destination_address: str, current_duration_min: int, prev_best_min: int):
    """Sends a formatted notification to a Slack channel."""
    if not SLACK_WEBHOOK_URL:
        logging.error("Slack Webhook URL is not configured.")
        return

    time_saved = prev_best_min - current_duration_min
    
    message = {
        "text": f"NEW RECORD TRAVEL TIME: {source_address} → {destination_address}",
        "blocks": [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🚨 New Record Travel Time! 🚨"
            }
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Route:*\n{source_address} → {destination_address}"},
                {"type": "mrkdwn", "text": f"*Time Saved:*\n*{time_saved} minute(s)*"},
                {"type": "mrkdwn", "text": f"*Current Estimate:*\n{current_duration_min} minutes"},
                {"type": "mrkdwn", "text": f"*Previous Best:*\n{prev_best_min} minutes"},
            ]
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "plain_text",
                    "text": f"Recorded at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    "emoji": True
                }
            ]
        }
    ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(SLACK_WEBHOOK_URL, json=message)
            response.raise_for_status()
        logging.info("Slack notification sent successfully.")
    except httpx.HTTPError as e:
        logging.error(f"Failed to send Slack notification: {e}")

async def get_live_travel_time(source_addr: str, dest_addr: str) -> Optional[int]:
    """Fetches live travel time from Google Maps using the Routes API."""
    if not API_KEY:
        logging.error("Google Maps API key is missing.")
        return None
        
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "routes.duration"
    }
    payload = {
        "origin": {"address": source_addr},
        "destination": {"address": dest_addr},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE"
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if "routes" in data and len(data["routes"]) > 0:
                duration_str = data["routes"][0]["duration"]
                return int(duration_str.rstrip('s'))
            else:
                logging.warning("No routes found in Google Maps API response.")
                return None
    except httpx.HTTPError as e:
        logging.error(f"Google Maps API request failed: {e}")
        return None
    except (KeyError, IndexError) as e:
        logging.error(f"Could not parse Google Maps API response: {e}")
        return None

# New scheduled function to record travel times
async def record_travel_times():
    """Fetches and records travel times for all configured routes."""
    logging.info("Running scheduled task to record travel times.")
    routes = load_routes()
    db_session = SessionLocal()
    try:
        for route in routes:
            source = route['source_address']
            destination = route['destination_address']
            duration_seconds = await get_live_travel_time(source, destination)
            if duration_seconds is not None:
                new_record = TravelRecord(
                    source=source,
                    destination=destination,
                    duration_seconds=duration_seconds,
                    timestamp=datetime.now()
                )
                db_session.add(new_record)
                logging.info(f"Recorded travel time for {source} -> {destination}: {duration_seconds // 60} mins.")
        db_session.commit()
        logging.info("Scheduled recording complete. Database updated.")
    except SQLAlchemyError as e:
        db_session.rollback()
        logging.error(f"Database error during scheduled task: {e}")
    finally:
        db_session.close()

# Initialize and configure the scheduler
scheduler = AsyncIOScheduler()
scheduler.add_job(
    record_travel_times,
    trigger=IntervalTrigger(minutes=15),
    id='record_travel_times',
    replace_existing=True
)


# --- API Endpoints ---
@app.get("/")
async def read_index():
    return FileResponse("ui/index.html")

@app.get("/routes", response_model=List[RouteEntry], summary="Get all routes")
async def get_routes():
    """Returns the list of all configured routes."""
    return load_routes()

@app.post("/add-route", response_model=Dict[str, str], status_code=201, summary="Add a new route")
async def add_route(request: AddRouteRequest):
    """Adds a new source-destination pair to the configuration."""
    routes = load_routes()
    if any(route['name'].lower() == request.route_name.lower() for route in routes):
        raise HTTPException(status_code=400, detail=f"Route with name '{request.route_name}' already exists.")

    new_route = {
        "name": request.route_name,
        "source_address": request.source_address,
        "destination_address": request.destination_address
    }
    routes.append(new_route)
    save_routes(routes)
    return {"status": "Route added successfully."}

@app.delete("/remove-route/{route_name}", response_model=Dict[str, str], summary="Remove a route")
async def remove_route(route_name: str):
    """Removes a route by its name from the configuration."""
    routes = load_routes()
    original_count = len(routes)
    routes = [route for route in routes if route['name'] != route_name]

    if len(routes) == original_count:
        raise HTTPException(status_code=404, detail=f"Route with name '{route_name}' not found.")
        
    save_routes(routes)
    return {"status": "Route removed successfully."}

@app.post("/check-travel-time")
async def check_travel_time(request: TravelRequest):
    source_address = request.source_address
    destination_address = request.destination_address
    route_key = f"{source_address.replace(' ', '')}-{destination_address.replace(' ', '')}"

    db_session = SessionLocal()
    try:
        best_record = db_session.query(BestTravelTime).filter_by(route_key=route_key).first()
        previous_best_seconds = best_record.duration_seconds if best_record else None

        current_duration_seconds = await get_live_travel_time(source_address, destination_address)

        if current_duration_seconds is None:
            return {"status": "Failed to fetch travel time from Google Maps."}
        
        current_duration_minutes = current_duration_seconds // 60
        prev_min_display = f"{previous_best_seconds // 60} mins" if previous_best_seconds is not None else "N/A"
        logging.info(f"Route: {route_key.upper()} | Current: {current_duration_minutes} mins | Record: {prev_min_display}")

        if previous_best_seconds is None or current_duration_seconds < previous_best_seconds:
            if best_record:
                best_record.duration_seconds = current_duration_seconds
                best_record.last_updated = datetime.now()
                logging.info("Updated best travel time record.")
            else:
                new_best_record = BestTravelTime(
                    route_key=route_key,
                    source=source_address,
                    destination=destination_address,
                    duration_seconds=current_duration_seconds
                )
                db_session.add(new_best_record)
                logging.info("Created new best travel time record.")

            db_session.commit()
            
            # Use the previous best for the "time saved" calculation
            previous_best_minutes = (previous_best_seconds // 60) if previous_best_seconds is not None else (current_duration_minutes + 5)
            await send_slack_notification(
                source_address=source_address,
                destination_address=destination_address,
                current_duration_min=current_duration_minutes,
                prev_best_min=previous_best_minutes
            )

            return {"status": "New minimum recorded.", "current_minutes": current_duration_minutes}
        else:
            return {"status": "No new minimum detected.", "current_minutes": current_duration_minutes, "record_minutes": previous_best_seconds // 60}
    except SQLAlchemyError as e:
        db_session.rollback()
        logging.error(f"Database error in /check-travel-time: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    finally:
        db_session.close()

@app.get("/historical-data/{source}/{destination}/{date_str}", summary="Get historical data for a route on a specific date")
def get_historical_data(source: str, destination: str, date_str: str):
    try:
        query_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    db_session = SessionLocal()
    try:
        records = db_session.query(TravelRecord).filter(
            TravelRecord.source == source,
            TravelRecord.destination == destination,
            text("DATE(timestamp) = :query_date")
        ).params(query_date=query_date).order_by(TravelRecord.timestamp).all()

        if not records:
            raise HTTPException(status_code=404, detail="No data found for this route on the specified date.")

        output = {
            "date": date_str,
            "data": [
                {
                    "time": record.timestamp.strftime("%H:%M:%S"),
                    "duration_minutes": record.duration_seconds // 60
                } for record in records
            ]
        }
        return output
    except SQLAlchemyError as e:
        logging.error(f"Database error retrieving historical data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    finally:
        db_session.close()

@app.on_event("startup")
async def startup_event():
    create_tables()
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    if scheduler.running:
        scheduler.shutdown()

# --- Local Run ---
if __name__ == "__main__":
    create_tables()
    scheduler.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)