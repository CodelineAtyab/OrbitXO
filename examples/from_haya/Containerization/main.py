import json
import os
import asyncio
import aiohttp
import csv
import io
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# ================== Load Environment Variables ==================
load_dotenv()

def get_maps_api_key() -> str | None:
    """
    Return the Google Maps API key from environment variables.
    Checks both MAPS_API_KEY and GOOGLE_MAPS_API_KEY.
    Returns None if not set.
    """
    key = os.getenv("MAPS_API_KEY") or os.getenv("GOOGLE_MAPS_API_KEY")
    if key:
        print("✅ Google Maps API key loaded successfully")
    else:
        print("⚠️ Warning: MAPS_API_KEY not found. Using mock/OSM fallback")
    return key

# ================== App Setup ==================
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

CONFIG_FILE = Path("routes_config.json")
if not CONFIG_FILE.exists():
    CONFIG_FILE.write_text("[]")

# ================== Google Maps API Functions ==================
async def get_travel_time(source_address: str, destination_address: str) -> str:
    """Get travel time from Google Maps Distance Matrix API"""
    api_key = get_maps_api_key()
    
    if not api_key:
        # fallback to mock data
        mock_times = ["8 min", "15 min", "25 min", "12 min", "18 min", "22 min", "1 hour 5 min", "45 min"]
        hash_value = hash(f"{source_address}{destination_address}") % len(mock_times)
        return mock_times[hash_value]
    
    try:
        base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": source_address,
            "destinations": destination_address,
            "mode": "driving",
            "departure_time": "now",
            "traffic_model": "best_guess",
            "key": api_key
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if (data.get("status") == "OK" and 
                        data.get("rows") and len(data["rows"]) > 0 and
                        data["rows"][0].get("elements") and
                        len(data["rows"][0]["elements"]) > 0):
                        
                        element = data["rows"][0]["elements"][0]
                        if element.get("status") == "OK":
                            duration_info = element.get("duration_in_traffic") or element.get("duration")
                            return duration_info.get("text", "N/A") if duration_info else "N/A"
                        elif element.get("status") == "ZERO_RESULTS":
                            return "No route found"
                        elif element.get("status") == "NOT_FOUND":
                            return "Address not found"
                    elif data.get("status") == "OVER_QUERY_LIMIT":
                        return "API quota exceeded"
                    elif data.get("status") == "REQUEST_DENIED":
                        return "Invalid API key"
        return "N/A"
    except Exception as e:
        print(f"❌ Error calling Google Maps API: {e}")
        return "Error"

# ================== Helper Functions ==================
def parse_time_to_minutes(time_str: str) -> float:
    """Convert time string to minutes (handles hours too)"""
    if not time_str or time_str in ["N/A", "Error", "No route found", "Address not found", "API quota exceeded", "Invalid API key"]:
        return 0
    try:
        total_minutes = 0
        time_str = time_str.lower()
        if "hour" in time_str:
            hour_part = time_str.split("hour")[0].strip()
            hours = float(hour_part.split()[-1]) if hour_part.split() else 0
            total_minutes += hours * 60
            remaining = time_str.split("hour")[1].strip() if "hour" in time_str else ""
            if "min" in remaining:
                min_part = remaining.split("min")[0].strip()
                minutes = float(min_part.split()[-1]) if min_part.split() else 0
                total_minutes += minutes
        elif "min" in time_str:
            min_part = time_str.split("min")[0].strip()
            total_minutes = float(min_part.split()[-1]) if min_part.split() else 0
        return total_minutes
    except Exception as e:
        print(f"Error parsing time '{time_str}': {e}")
        return 0

def format_minutes_to_time(minutes: float) -> str:
    """Convert minutes back to readable time format"""
    if minutes <= 0:
        return "N/A"
    if minutes >= 60:
        hours = int(minutes // 60)
        remaining_minutes = int(minutes % 60)
        if remaining_minutes > 0:
            return f"{hours} hour {remaining_minutes} min"
        else:
            return f"{hours} hour"
    else:
        return f"{int(minutes)} min"

async def update_route_times(routes: list) -> list:
    """Update travel times and statistics"""
    for route in routes:
        try:
            travel_time = await get_travel_time(route["source_address"], route["destination_address"])
            route["travel_time"] = travel_time
            current_min = parse_time_to_minutes(travel_time)
            if "recorded_times" not in route:
                route["recorded_times"] = []
            if current_min > 0:
                route["recorded_times"].append({
                    "time": travel_time,
                    "minutes": current_min,
                    "timestamp": datetime.now().isoformat()
                })
                route["recorded_times"] = route["recorded_times"][-50:]
            if route["recorded_times"]:
                times = [r["minutes"] for r in route["recorded_times"]]
                route["average_time"] = format_minutes_to_time(sum(times)/len(times))
                route["best_time"] = format_minutes_to_time(min(times))
                route["worst_time"] = format_minutes_to_time(max(times))
                route["previous_best"] = format_minutes_to_time(min(times))
                route["time_saved"] = max(0, max(times)-current_min) if len(times) > 1 else 0
            else:
                route["average_time"] = "N/A"
                route["best_time"] = "N/A"
                route["worst_time"] = "N/A"
                route["previous_best"] = route.get("previous_best", "N/A")
                route["time_saved"] = 0
            route["last_recorded"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(f"Error updating route {route.get('source_name', 'Unknown')}: {e}")
            route["travel_time"] = "Error"
            route["last_recorded"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return routes

# ================== Config Helpers ==================
def load_routes():
    try:
        with open(CONFIG_FILE, "r", encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_routes(routes):
    with open(CONFIG_FILE, "w", encoding='utf-8') as f:
        json.dump(routes, f, indent=4, ensure_ascii=False)

def validate_address(address: str) -> bool:
    return bool(address and len(address.strip()) >= 4)

def validate_name(name: str) -> bool:
    return bool(name and len(name.strip()) >= 2 and len(name.strip()) <= 50)

# ================== Startup Event ==================
@app.on_event("startup")
async def startup_event():
    get_maps_api_key()  # Check key
    if not CONFIG_FILE.exists():
        save_routes([])
    await run_migrations()
    print("🚀 Route Monitor started successfully!")

# ================== Migrations & Cleanup ==================
def cleanup_old_data():
    try:
        routes = load_routes()
        for route in routes:
            if "recorded_times" in route and len(route["recorded_times"]) > 50:
                route["recorded_times"] = route["recorded_times"][-50:]
        save_routes(routes)
    except Exception as e:
        print(f"Cleanup error: {e}")

def migrate_old_format():
    try:
        routes = load_routes()
        for route in routes:
            if "recorded_times" not in route:
                route["recorded_times"] = []
            for field in ["best_time","average_time","worst_time","previous_best","time_saved","created_at"]:
                if field not in route:
                    route[field] = "N/A" if field!="time_saved" else 0
        save_routes(routes)
    except Exception as e:
        print(f"Migration error: {e}")

async def run_migrations():
    migrate_old_format()
    cleanup_old_data()

# ================== Endpoints ==================
@app.get("/")
async def index():
    try:
        with open("static/index.html","r",encoding="utf-8") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        return HTMLResponse("<h1>Error: index.html not found in static/</h1>", status_code=404)

@app.get("/refresh")
async def refresh_times():
    routes = load_routes()
    routes = await update_route_times(routes)
    save_routes(routes)
    return RedirectResponse("/?success=refreshed", status_code=303)

@app.get("/health")
async def health_check():
    return {
        "status":"healthy",
        "api_key_configured": bool(get_maps_api_key()),
        "routes_count": len(load_routes()),
        "config_file_exists": CONFIG_FILE.exists(),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/routes")
async def get_routes_api():
    """Get all routes as JSON"""
    routes = load_routes()
    return {"status": "success", "routes": routes}

@app.post("/add_route")
async def add_route(
    source_name: str = Form(...),
    source_address: str = Form(...),
    destination_name: str = Form(...),
    destination_address: str = Form(...)
):
    """Add a new route"""
    if not all([validate_name(source_name), validate_name(destination_name),
                validate_address(source_address), validate_address(destination_address)]):
        return RedirectResponse("/?error=invalid_input", status_code=303)

    routes = load_routes()
    new_route = {
        "source_name": source_name.strip(),
        "source_address": source_address.strip(),
        "destination_name": destination_name.strip(),
        "destination_address": destination_address.strip(),
        "travel_time": "Pending...",
        "recorded_times": [],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    routes.append(new_route)
    routes = await update_route_times(routes)
    save_routes(routes)
    return RedirectResponse("/?success=route_added", status_code=303)

@app.post("/delete_route")
async def delete_route(index: int = Form(...)):
    """Delete a route by index"""
    routes = load_routes()
    if 0 <= index < len(routes):
        routes.pop(index)
        save_routes(routes)
    return RedirectResponse("/?success=deleted", status_code=303)

@app.post("/clear_routes")
async def clear_routes():
    """Clear all routes"""
    save_routes([])
    return RedirectResponse("/?success=cleared", status_code=303)

# ================== Run Server ==================
if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST","0.0.0.0")
    port = int(os.getenv("PORT",8000))
    debug_mode = os.getenv("DEBUG","false").lower() == "true"
    uvicorn.run(app, host=host, port=port, reload=debug_mode)
