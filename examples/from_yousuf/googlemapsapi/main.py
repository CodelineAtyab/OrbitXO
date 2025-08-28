import os
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
import uvicorn
from pathlib import Path

from googlemapapi import get_travel_time, load_locations_from_config
from timetracker import check_and_notify_new_minimum
from logger import configure_logging, get_logger
from database import init_db, insert_route

configure_logging(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = get_logger(__name__)

init_db()

app = FastAPI(title="Google Maps ETA Tracker")

@app.get("/", response_class=HTMLResponse, tags=["ui"])
def root_ui():
	"""Serve the single-page UI (ui.html) as the front page."""
	ui_path = Path(__file__).parent / "ui.html"
	if not ui_path.exists():
		return HTMLResponse("<h1>UI not found</h1>", status_code=500)
	return HTMLResponse(ui_path.read_text(encoding="utf-8"))

@app.get("/route", tags=["route"])
def get_route(source: Optional[str] = Query(None), destination: Optional[str] = Query(None)):
	"""
	Compute travel time between source and destination.
	If source/destination are omitted, load from config.
	"""
	if not source or not destination:
		cfg_source, cfg_destination = load_locations_from_config()
		source = source or cfg_source
		destination = destination or cfg_destination

	logger.info("Requesting travel time from %s to %s", source, destination)
	result = get_travel_time(source, destination)
	if not result.get("success"):
		logger.error("Error getting travel time: %s", result.get("error"))
		logger.debug("Details: %s", result.get("details"))
		raise HTTPException(status_code=502, detail={"error": result.get("error"), "details": result.get("details")})

	duration_seconds = result.get("duration_value", 0)
	duration_minutes = int(round(duration_seconds / 60)) if duration_seconds else 0

	update_result = check_and_notify_new_minimum(result['source'], result['destination'], duration_minutes)
	notification_sent = bool(update_result.get("notification_sent"))
	new_minimum = bool(update_result.get("new_minimum"))

	inserted_id = None
	try:
		inserted_id = insert_route(
			origin=result.get("source", source),
			destination=result.get("destination", destination),
			duration_text=result.get("duration"),
			duration_value=duration_seconds,
			distance_text=result.get("distance"),
			distance_value=result.get("distance_value"),
		)
		logger.debug("Route recorded in DB with id=%s", inserted_id)
	except Exception as e:
		logger.warning("Failed to record route in DB: %s", e)

	response = {
		"source": result.get("source"),
		"destination": result.get("destination"),
		"distance_text": result.get("distance"),
		"distance_value": result.get("distance_value"),
		"duration_text": result.get("duration"),
		"duration_seconds": duration_seconds,
		"duration_minutes": duration_minutes,
		"new_minimum": new_minimum,
		"notification_sent": notification_sent,
		"db_id": inserted_id,
	}

	return response

if __name__ == "__main__":
	uvicorn.run(
		app,
		host="0.0.0.0",
		port=int(os.environ.get("PORT", 8000)),
		reload=bool(os.environ.get("RELOAD", False)),
	)
