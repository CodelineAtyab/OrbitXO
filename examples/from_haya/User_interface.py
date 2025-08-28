import json
import os
import asyncio
import aiohttp
import csv
import io
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse, StreamingResponse
from jinja2 import Environment, DictLoader
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = FastAPI()

# ================== Config File ==================
CONFIG_FILE = Path("routes_config.json")
if not CONFIG_FILE.exists():
    CONFIG_FILE.write_text("[]")

# ================== Google Maps API Functions ==================
async def get_travel_time(source_address: str, destination_address: str) -> str:
    """Get travel time from Google Maps Distance Matrix API"""
    api_key = os.getenv("MAPS_API_KEY")
    
    if not api_key:
        print("⚠️ Warning: MAPS_API_KEY not found, using mock data")
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

def parse_time_to_minutes(time_str: str) -> float:
    """Convert time string to minutes (handles hours too)"""
    if not time_str or time_str in ["N/A", "Error", "No route found", "Address not found", "API quota exceeded", "Invalid API key"]:
        return 0
    
    try:
        total_minutes = 0
        time_str = time_str.lower()
        
        # Handle hours and minutes
        if "hour" in time_str:
            # Extract hours
            hour_part = time_str.split("hour")[0].strip()
            hours = float(hour_part.split()[-1]) if hour_part.split() else 0
            total_minutes += hours * 60
            
            # Check for remaining minutes
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
    """Update travel times with enhanced statistics tracking"""
    for route in routes:
        try:
            travel_time = await get_travel_time(route["source_address"], route["destination_address"])
            route["travel_time"] = travel_time
            
            current_min = parse_time_to_minutes(travel_time)
            
            # Track all recorded times for statistics
            if "recorded_times" not in route:
                route["recorded_times"] = []
            
            if current_min > 0:
                route["recorded_times"].append({
                    "time": travel_time,
                    "minutes": current_min,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Keep only last 50 records to prevent unlimited growth
                route["recorded_times"] = route["recorded_times"][-50:]
            
            # Calculate statistics
            if route["recorded_times"]:
                times = [r["minutes"] for r in route["recorded_times"]]
                route["average_time"] = format_minutes_to_time(sum(times) / len(times))
                route["best_time"] = format_minutes_to_time(min(times))
                route["worst_time"] = format_minutes_to_time(max(times))
                
                # Update previous best
                best_minutes = min(times)
                route["previous_best"] = format_minutes_to_time(best_minutes)
                
                # Calculate time saved compared to worst time
                if len(times) > 1:
                    worst_minutes = max(times)
                    route["time_saved"] = max(0, worst_minutes - current_min)
                else:
                    route["time_saved"] = 0
            else:
                # No valid times recorded
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

# ================== Templates ==================
templates_dict = {
    "layout.html": """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Route Monitor</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
.container { max-width: 1400px; margin: 0 auto; background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden; }
.header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
.header h1 { margin: 0; font-size: 2.5em; font-weight: 300; }
.header p { margin: 10px 0 0 0; opacity: 0.9; }
.content { padding: 30px; }
.error-message { background: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; margin-bottom: 20px; border: 1px solid #f5c6cb; }
.success-message { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin-bottom: 20px; border: 1px solid #c3e6cb; }
table { border-collapse: collapse; width: 100%; margin-bottom: 30px; border-radius: 10px; overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
th, td { padding: 12px; text-align: left; border-bottom: 1px solid #e9ecef; font-size: 0.9em; }
th { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; font-weight: 500; }
tr:nth-child(even) { background-color: #f8f9fa; }
tr:hover { background-color: #e9ecef; }
.time-badge { background: #28a745; color: white; padding: 4px 8px; border-radius: 12px; font-weight: bold; font-size: 0.8em; display: inline-block; }
.time-error { background: #dc3545; }
.time-warning { background: #ffc107; color: #212529; }
.section-title { font-size: 1.8em; margin: 30px 0 20px 0; color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; }
.button-group { margin-bottom: 20px; display: flex; gap: 10px; flex-wrap: wrap; }
form { background: #f8f9fa; padding: 25px; border-radius: 10px; margin-top: 20px; border: 1px solid #e9ecef; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
.form-group { display: flex; flex-direction: column; }
.form-group label { margin-bottom: 5px; font-weight: 500; color: #333; }
input[type="text"], input[type="number"] { padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 1em; transition: border-color 0.3s; }
input[type="text"]:focus, input[type="number"]:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2); }
.btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 10px 20px; border-radius: 20px; cursor: pointer; font-size: 0.9em; font-weight: 500; transition: transform 0.2s, box-shadow 0.2s; text-decoration: none; display: inline-block; }
.btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4); color: white; }
.btn-danger { background: #dc3545; }
.btn-danger:hover { background: #c82333; box-shadow: 0 5px 15px rgba(220, 53, 69, 0.4); }
.btn-success { background: #28a745; }
.btn-success:hover { background: #218838; }
.btn-info { background: #17a2b8; }
.btn-info:hover { background: #138496; }
.btn-warning { background: #ffc107; color: #212529; }
.btn-warning:hover { background: #e0a800; }
.btn-sm { padding: 6px 12px; font-size: 0.8em; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; margin: 10px 0; }
.stat-card { background: #f8f9fa; padding: 8px 12px; border-radius: 8px; text-align: center; border: 1px solid #e9ecef; }
.stat-card strong { color: #667eea; }
.route-info { display: flex; align-items: center; gap: 8px; font-weight: 500; }
.arrow { color: #667eea; font-weight: bold; font-size: 1.1em; }
.empty-state { text-align: center; padding: 60px 20px; color: #6c757d; }
.empty-state h3 { font-size: 1.5em; margin-bottom: 10px; }
.auto-refresh-info { background: #e7f3ff; border: 1px solid #bee5eb; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
.auto-refresh-controls { display: flex; align-items: center; gap: 15px; flex-wrap: wrap; }
@media (max-width: 768px) { 
    .form-row { grid-template-columns: 1fr; } 
    table { font-size: 0.8em; } 
    th, td { padding: 8px; } 
    .button-group { flex-direction: column; align-items: stretch; }
    .auto-refresh-controls { flex-direction: column; align-items: stretch; }
    .stats-grid { grid-template-columns: 1fr 1fr; }
}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🗺️ Route Monitor</h1>
        <p>Track real-time travel times with Google Maps API</p>
    </div>
    <div class="content">
        {% block content %}{% endblock %}
    </div>
</div>
<script>
let autoRefreshInterval = null;

function enableAutoRefresh(minutes) {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
    
    if (minutes > 0) {
        autoRefreshInterval = setInterval(async () => {
            try {
                const response = await fetch('/auto-refresh');
                if (response.ok) {
                    location.reload();
                }
            } catch (error) {
                console.error('Auto-refresh failed:', error);
            }
        }, minutes * 60 * 1000);
        
        document.getElementById('refresh-status').textContent = `Auto-refresh enabled (${minutes} min intervals)`;
        document.getElementById('refresh-status').style.color = '#28a745';
    } else {
        document.getElementById('refresh-status').textContent = 'Auto-refresh disabled';
        document.getElementById('refresh-status').style.color = '#6c757d';
    }
}

function toggleAutoRefresh() {
    const select = document.getElementById('auto-refresh-select');
    const minutes = parseInt(select.value);
    enableAutoRefresh(minutes);
}
</script>
</body>
</html>
""",
    "index.html": """
{% extends "layout.html" %}
{% block content %}

{% if error %}
<div class="error-message">{{ error }}</div>
{% endif %}

<div class="auto-refresh-info">
    <div class="auto-refresh-controls">
        <label for="auto-refresh-select"><strong>🔄 Auto-refresh:</strong></label>
        <select id="auto-refresh-select" onchange="toggleAutoRefresh()" style="padding: 8px; border-radius: 4px; border: 1px solid #ddd;">
            <option value="0">Disabled</option>
            <option value="1">Every 1 minute</option>
            <option value="5">Every 5 minutes</option>
            <option value="10">Every 10 minutes</option>
            <option value="15">Every 15 minutes</option>
            <option value="30">Every 30 minutes</option>
        </select>
        <span id="refresh-status" style="color: #6c757d;">Auto-refresh disabled</span>
    </div>
</div>

<div class="button-group">
    <a href="/refresh" class="btn btn-info">🔄 Refresh Now</a>
    <a href="/export" class="btn btn-success">📊 Export CSV</a>
    {% if routes %}
    <form action="/clear_all_routes" method="post" style="display: inline; background: none; padding: 0; margin: 0; border: none;">
        <button type="submit" class="btn btn-danger" onclick="return confirm('Are you sure you want to delete ALL routes? This cannot be undone.')">🗑️ Clear All</button>
    </form>
    <form action="/reset_statistics" method="post" style="display: inline; background: none; padding: 0; margin: 0; border: none;">
        <button type="submit" class="btn btn-warning" onclick="return confirm('Reset all statistics? This will clear historical data.')">📊 Reset Stats</button>
    </form>
    {% endif %}
</div>

<h2 class="section-title">📍 Current Routes ({{ routes|length }})</h2>

{% if routes %}
<div style="overflow-x: auto;">
<table>
<tr>
    <th>Route</th>
    <th>Current Time</th>
    <th>Statistics</th>
    <th>Last Updated</th>
    <th>Actions</th>
</tr>
{% for route in routes %}
<tr>
<td>
    <div class="route-info">
        <span>🛣️ {{ route.source_name }}</span>
        <span class="arrow">→</span>
        <span>{{ route.destination_name }}</span>
    </div>
    <div style="font-size: 0.8em; color: #6c757d; margin-top: 5px;">
        <div>📍 {{ route.source_address }}</div>
        <div>🎯 {{ route.destination_address }}</div>
    </div>
</td>
<td>
    {% set time = route.travel_time %}
    {% if time and time not in ["N/A", "Error", "No route found", "Address not found"] %}
        <span class="time-badge">⏱️ {{ time }}</span>
    {% elif time in ["Error", "No route found", "Address not found"] %}
        <span class="time-badge time-error">❌ {{ time }}</span>
    {% else %}
        <span class="time-badge time-warning">⚠️ N/A</span>
    {% endif %}
    {% if route.time_saved and route.time_saved > 0 %}
        <div style="font-size: 0.8em; color: #28a745; margin-top: 5px;">
            💡 Saved {{ "%.1f"|format(route.time_saved) }} min vs worst
        </div>
    {% endif %}
</td>
<td>
    <div class="stats-grid">
        <div class="stat-card">
            <strong>Best:</strong><br>
            🏆 {{ route.best_time if route.best_time else "N/A" }}
        </div>
        <div class="stat-card">
            <strong>Avg:</strong><br>
            📊 {{ route.average_time if route.average_time else "N/A" }}
        </div>
        <div class="stat-card">
            <strong>Worst:</strong><br>
            📈 {{ route.worst_time if route.worst_time else "N/A" }}
        </div>
    </div>
    {% if route.recorded_times %}
    <div style="font-size: 0.8em; color: #6c757d;">
        📈 {{ route.recorded_times|length }} data points
    </div>
    {% endif %}
</td>
<td style="font-size: 0.9em;">
    📅 {{ route.last_recorded if route.last_recorded else "Never" }}
</td>
<td>
    <form action="/delete_route" method="post" style="display: inline; background: none; padding: 0; margin: 0; border: none;">
        <input type="hidden" name="index" value="{{ loop.index0 }}">
        <button type="submit" class="btn btn-danger btn-sm" onclick="return confirm('Delete route: {{ route.source_name }} → {{ route.destination_name }}?')">
            🗑️ Delete
        </button>
    </form>
</td>
</tr>
{% endfor %}
</table>
</div>
{% else %}
<div class="empty-state">
    <h3>📭 No saved routes</h3>
    <p>Add your first route below to start monitoring travel times!</p>
</div>
{% endif %}

<h2 class="section-title">➕ Add New Route</h2>
<form action="/add_route" method="post">
    <div class="form-row">
        <div class="form-group">
            <label for="source_name">🏠 Source Name:</label>
            <input type="text" id="source_name" name="source_name" placeholder="e.g., Home, Office A" required maxlength="50">
        </div>
        <div class="form-group">
            <label for="destination_name">🎯 Destination Name:</label>
            <input type="text" id="destination_name" name="destination_name" placeholder="e.g., Work, Mall, Airport" required maxlength="50">
        </div>
    </div>
    
    <div class="form-row">
        <div class="form-group">
            <label for="source_address">📍 Source Address:</label>
            <input type="text" id="source_address" name="source_address" placeholder="123 Main St, Muscat, Oman" required>
        </div>
        <div class="form-group">
            <label for="destination_address">📍 Destination Address:</label>
            <input type="text" id="destination_address" name="destination_address" placeholder="456 Work Ave, Muscat, Oman" required>
        </div>
    </div>
    
    <div style="text-align: right;">
        <button type="submit" class="btn">➕ Add Route</button>
    </div>
</form>

{% endblock %}
"""
}

env = Environment(loader=DictLoader(templates_dict))

# ================== Helper Functions ==================
def load_routes():
    try:
        with open(CONFIG_FILE, "r", encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_routes(routes):
    with open(CONFIG_FILE, "w", encoding='utf-8') as f:
        json.dump(routes, f, indent=4, ensure_ascii=False)

def render_template(name, **context):
    template = env.get_template(name)
    return HTMLResponse(template.render(**context))

def validate_address(address: str) -> bool:
    """Enhanced address validation"""
    return bool(address and len(address.strip()) >= 4)

def validate_name(name: str) -> bool:
    """Validate route name"""
    return bool(name and len(name.strip()) >= 2 and len(name.strip()) <= 50)

# ================== Startup Event ==================
@app.on_event("startup")
async def startup_event():
    """Check API key and setup on startup"""
    api_key = os.getenv("MAPS_API_KEY")
    if api_key:
        print("✅ Google Maps API key loaded successfully")
    else:
        print("⚠️ Warning: MAPS_API_KEY not found in .env file")
        print("   The app will use mock travel times instead")
    
    # Ensure config file exists
    if not CONFIG_FILE.exists():
        save_routes([])
    
    print("🚀 Route Monitor started successfully!")

# ================== Main Endpoints ==================
@app.get("/")
async def index(request: Request):
    routes = load_routes()
    error = request.query_params.get("error")
    error_messages = {
        "empty_names": "❌ Route names cannot be empty and must be 2-50 characters long",
        "invalid_address": "❌ Please enter valid addresses (at least 4 characters each)",
        "duplicate": "❌ This route combination already exists",
        "api_error": "❌ Error connecting to Google Maps API",
        "invalid_input": "❌ Please check your input and try again"
    }
    error_message = error_messages.get(error) if error else None
    return render_template("index.html", routes=routes, error=error_message)

@app.get("/refresh")
async def refresh_times():
    """Manual refresh of all route times"""
    try:
        routes = load_routes()
        routes = await update_route_times(routes)
        save_routes(routes)
        return RedirectResponse("/?success=refreshed", status_code=303)
    except Exception as e:
        print(f"Error during refresh: {e}")
        return RedirectResponse("/?error=api_error", status_code=303)

@app.get("/auto-refresh")
async def auto_refresh():
    """API endpoint for auto-refreshing times"""
    try:
        routes = load_routes()
        routes = await update_route_times(routes)
        save_routes(routes)
        return {"status": "success", "routes_count": len(routes), "timestamp": datetime.now().isoformat()}
    except Exception as e:
        print(f"Auto-refresh error: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/export")
async def export_routes():
    """Export routes data as CSV"""
    routes = load_routes()
    if not routes:
        return RedirectResponse("/?error=no_data", status_code=303)
    
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Source Name', 'Destination Name', 'Source Address', 'Destination Address',
            'Current Time', 'Best Time', 'Average Time', 'Worst Time', 
            'Time Saved (min)', 'Data Points', 'Last Updated'
        ])
        
        # Write data
        for route in routes:
            writer.writerow([
                route.get('source_name', ''),
                route.get('destination_name', ''),
                route.get('source_address', ''),
                route.get('destination_address', ''),
                route.get('travel_time', 'N/A'),
                route.get('best_time', 'N/A'),
                route.get('average_time', 'N/A'),
                route.get('worst_time', 'N/A'),
                f"{route.get('time_saved', 0):.1f}",
                len(route.get('recorded_times', [])),
                route.get('last_recorded', 'Never')
            ])
        
        output.seek(0)
        filename = f"routes_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        print(f"Export error: {e}")
        return RedirectResponse("/?error=export_failed", status_code=303)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    api_key = os.getenv("MAPS_API_KEY")
    routes_count = len(load_routes())
    
    return {
        "status": "healthy",
        "api_key_configured": bool(api_key),
        "routes_count": routes_count,
        "config_file_exists": CONFIG_FILE.exists(),
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }

# ================== Route Management Endpoints ==================
@app.post("/add_route")
async def add_route(
    source_name: str = Form(...),
    source_address: str = Form(...),
    destination_name: str = Form(...),
    destination_address: str = Form(...)
):
    try:
        # Validate inputs
        if not validate_name(source_name) or not validate_name(destination_name):
            return RedirectResponse("/?error=empty_names", status_code=303)
        
        if not validate_address(source_address) or not validate_address(destination_address):
            return RedirectResponse("/?error=invalid_address", status_code=303)
        
        routes = load_routes()
        
        # Check for duplicates (case insensitive)
        source_clean = source_name.strip().lower()
        dest_clean = destination_name.strip().lower()
        
        for route in routes:
            if (route["source_name"].lower() == source_clean and 
                route["destination_name"].lower() == dest_clean):
                return RedirectResponse("/?error=duplicate", status_code=303)
        
        # Create new route
        new_route = {
            "source_name": source_name.strip(),
            "source_address": source_address.strip(),
            "destination_name": destination_name.strip(),
            "destination_address": destination_address.strip(),
            "recorded_times": [],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Get initial travel time
        travel_time = await get_travel_time(new_route["source_address"], new_route["destination_address"])
        new_route["travel_time"] = travel_time
        new_route["last_recorded"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Initialize statistics
        current_min = parse_time_to_minutes(travel_time)
        if current_min > 0:
            new_route["recorded_times"] = [{
                "time": travel_time,
                "minutes": current_min,
                "timestamp": datetime.now().isoformat()
            }]
            new_route["best_time"] = travel_time
            new_route["average_time"] = travel_time
            new_route["worst_time"] = travel_time
            new_route["previous_best"] = travel_time
            new_route["time_saved"] = 0
        else:
            new_route["best_time"] = "N/A"
            new_route["average_time"] = "N/A"
            new_route["worst_time"] = "N/A"
            new_route["previous_best"] = "N/A"
            new_route["time_saved"] = 0
        
        routes.append(new_route)
        save_routes(routes)
        return RedirectResponse("/?success=route_added", status_code=303)
        
    except Exception as e:
        print(f"Error adding route: {e}")
        return RedirectResponse("/?error=invalid_input", status_code=303)

@app.post("/delete_route")
async def delete_route(index: int = Form(...)):
    """Delete a specific route"""
    try:
        routes = load_routes()
        if 0 <= index < len(routes):
            deleted_route = routes.pop(index)
            save_routes(routes)
            print(f"Deleted route: {deleted_route.get('source_name', 'Unknown')} → {deleted_route.get('destination_name', 'Unknown')}")
            return RedirectResponse("/?success=route_deleted", status_code=303)
        else:
            return RedirectResponse("/?error=invalid_route", status_code=303)
    except Exception as e:
        print(f"Error deleting route: {e}")
        return RedirectResponse("/?error=delete_failed", status_code=303)

@app.post("/clear_all_routes")
async def clear_all_routes():
    """Clear all routes"""
    try:
        routes_count = len(load_routes())
        save_routes([])
        print(f"Cleared {routes_count} routes")
        return RedirectResponse("/?success=all_cleared", status_code=303)
    except Exception as e:
        print(f"Error clearing routes: {e}")
        return RedirectResponse("/?error=clear_failed", status_code=303)

@app.post("/reset_statistics")
async def reset_statistics():
    """Reset all time statistics while keeping routes"""
    try:
        routes = load_routes()
        reset_count = 0
        
        for route in routes:
            # Keep basic route info but reset statistics
            if any(key in route for key in ["recorded_times", "previous_best", "time_saved", "average_time", "best_time", "worst_time"]):
                route.pop("recorded_times", None)
                route.pop("previous_best", None)
                route.pop("time_saved", None)
                route.pop("average_time", None)
                route.pop("best_time", None)
                route.pop("worst_time", None)
                
                # Reset to initial values
                route["recorded_times"] = []
                route["previous_best"] = "N/A"
                route["time_saved"] = 0
                route["average_time"] = "N/A"
                route["best_time"] = "N/A"
                route["worst_time"] = "N/A"
                reset_count += 1
        
        save_routes(routes)
        print(f"Reset statistics for {reset_count} routes")
        return RedirectResponse("/?success=stats_reset", status_code=303)
        
    except Exception as e:
        print(f"Error resetting statistics: {e}")
        return RedirectResponse("/?error=reset_failed", status_code=303)

# ================== API Endpoints for External Integration ==================
@app.get("/api/routes")
async def get_routes_api():
    """Get all routes as JSON (API endpoint)"""
    try:
        routes = load_routes()
        return {
            "status": "success",
            "count": len(routes),
            "routes": routes,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/routes/{route_index}")
async def get_route_api(route_index: int):
    """Get specific route by index (API endpoint)"""
    try:
        routes = load_routes()
        if 0 <= route_index < len(routes):
            return {
                "status": "success",
                "route": routes[route_index],
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {"status": "error", "message": "Route not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/refresh")
async def refresh_api():
    """Refresh all routes via API"""
    try:
        routes = load_routes()
        routes = await update_route_times(routes)
        save_routes(routes)
        return {
            "status": "success",
            "message": "Routes refreshed successfully",
            "count": len(routes),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ================== Error Handlers ==================
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 handler"""
    return render_template("index.html", routes=[], error="Page not found - redirected to home")

@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    """Custom 500 handler"""
    print(f"Server error: {exc}")
    return render_template("index.html", routes=[], error="Server error occurred - please try again")

# ================== Development Helpers ==================
@app.get("/debug")
async def debug_info():
    """Debug endpoint for development"""
    if os.getenv("DEBUG") != "true":
        return {"error": "Debug mode not enabled"}
    
    try:
        routes = load_routes()
        api_key = os.getenv("MAPS_API_KEY")
        
        debug_data = {
            "config_file": str(CONFIG_FILE),
            "config_exists": CONFIG_FILE.exists(),
            "routes_count": len(routes),
            "api_key_length": len(api_key) if api_key else 0,
            "sample_route": routes[0] if routes else None,
            "environment_vars": {
                "MAPS_API_KEY": "***" if api_key else None,
                "DEBUG": os.getenv("DEBUG"),
                "PORT": os.getenv("PORT", "8000")
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return debug_data
        
    except Exception as e:
        return {"error": str(e)}

# ================== Run Server ==================
if __name__ == "__main__":
    import uvicorn
    
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug_mode = os.getenv("DEBUG", "false").lower() == "true"
    
    print(f"🌐 Starting Route Monitor on {host}:{port}")
    print(f"🔧 Debug mode: {debug_mode}")
    
    try:
        uvicorn.run(
            app, 
            host=host, 
            port=port,
            reload=debug_mode,
            log_level="info" if not debug_mode else "debug"
        )
    except KeyboardInterrupt:
        print("\n👋 Route Monitor stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

# ================== Additional Utilities ==================
def cleanup_old_data():
    """Utility function to clean up old recorded times (can be called periodically)"""
    try:
        routes = load_routes()
        cleaned_count = 0
        
        for route in routes:
            if "recorded_times" in route and len(route["recorded_times"]) > 100:
                # Keep only the latest 50 records
                route["recorded_times"] = route["recorded_times"][-50:]
                cleaned_count += 1
        
        if cleaned_count > 0:
            save_routes(routes)
            print(f"🧹 Cleaned old data from {cleaned_count} routes")
        
        return cleaned_count
        
    except Exception as e:
        print(f"Error during cleanup: {e}")
        return 0

def migrate_old_format():
    """Migrate routes from old format to new format (backward compatibility)"""
    try:
        routes = load_routes()
        migrated_count = 0
        
        for route in routes:
            # Check if route needs migration
            needs_migration = False
            
            # Add missing fields
            if "recorded_times" not in route:
                route["recorded_times"] = []
                needs_migration = True
            
            if "created_at" not in route:
                route["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                needs_migration = True
            
            # Ensure all statistics fields exist
            for field in ["best_time", "average_time", "worst_time", "previous_best", "time_saved"]:
                if field not in route:
                    route[field] = "N/A" if field != "time_saved" else 0
                    needs_migration = True
            
            if needs_migration:
                migrated_count += 1
        
        if migrated_count > 0:
            save_routes(routes)
            print(f"🔄 Migrated {migrated_count} routes to new format")
        
        return migrated_count
        
    except Exception as e:
        print(f"Error during migration: {e}")
        return 0

# ================== Startup Migration ==================
@app.on_event("startup")
async def run_migrations():
    """Run any necessary migrations on startup"""
    try:
        # Run migration for backward compatibility
        migrate_old_format()
        
        # Clean up old data
        cleanup_old_data()
        
    except Exception as e:
        print(f"Migration error: {e}")