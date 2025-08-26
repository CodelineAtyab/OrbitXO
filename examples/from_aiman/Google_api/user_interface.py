import os
import json
import uvicorn
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from database_Integration import TravelTimeDatabase
from google_maps_api import get_travel_time

app = FastAPI(title="Route Monitor")

templates_dir = os.path.join(os.path.dirname(__file__), "templates")
os.makedirs(templates_dir, exist_ok=True)
templates = Jinja2Templates(directory=templates_dir)

static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
DATABASE_FILE = os.path.join(os.path.dirname(__file__), "travel_times.db")

class Route(BaseModel):
    source_name: str
    source_address: str
    destination_name: str
    destination_address: str

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {
            "api_key": "",
            "routes": []
        }
    
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def validate_address(address):
    try:
        result = get_travel_time(address, address)
        return True
    except Exception as e:
        return False

@app.get("/")
async def home(request: Request):
    config = load_config()
    routes = config.get("routes", [])
    
    db = TravelTimeDatabase(DATABASE_FILE)
    
    route_data = []
    for route in routes:
        source = route["source"]
        destination = route["destination"]
        
        try:
            latest_time = db.get_latest_travel_time(source, destination)
            duration = latest_time[2] if latest_time else "N/A"
        except:
            duration = "N/A"
            
        route_data.append({
            "source_name": source.split(",")[0] if "," in source else source,
            "source_address": source,
            "destination_name": destination.split(",")[0] if "," in destination else destination,
            "destination_address": destination,
            "duration": duration
        })
    
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "routes": route_data, "api_key": config.get("api_key", "")}
    )

@app.post("/add-route")
async def add_route(
    source_name: str = Form(...),
    source_address: str = Form(...),
    destination_name: str = Form(...),
    destination_address: str = Form(...)
):
    if not source_address or not destination_address:
        raise HTTPException(status_code=400, detail="Source and destination addresses are required")
    
    if not validate_address(source_address) or not validate_address(destination_address):
        raise HTTPException(status_code=400, detail="Invalid address")
    
    config = load_config()
    
    new_route = {
        "source": source_address,
        "destination": destination_address
    }
    
    if "routes" not in config:
        config["routes"] = []
    
    if new_route not in config["routes"]:
        config["routes"].append(new_route)
        save_config(config)
    
    return RedirectResponse(url="/", status_code=303)

@app.post("/remove-route")
async def remove_route(
    source_address: str = Form(...),
    destination_address: str = Form(...)
):
    config = load_config()
    
    routes = config.get("routes", [])
    config["routes"] = [r for r in routes if not (r["source"] == source_address and r["destination"] == destination_address)]
    
    save_config(config)
    
    return RedirectResponse(url="/", status_code=303)

@app.post("/update-api-key")
async def update_api_key(api_key: str = Form(...)):
    config = load_config()
    config["api_key"] = api_key
    save_config(config)
    
    return RedirectResponse(url="/", status_code=303)

def get_latest_travel_time(db, source, destination):
    try:
        return db.get_latest_travel_time(source, destination)
    except:
        db._init_db()
        try:
            return db.get_latest_travel_time(source, destination)
        except:
            return None

def create_template_files():
   
    index_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Route Monitor</title>
        <link rel="stylesheet" href="/static/styles.css">
    </head>
    <body>
        <div class="container">
            <h1>Route Monitor</h1>
            
            <div class="card">
                <h2>API Key Configuration</h2>
                <form action="/update-api-key" method="post">
                    <div class="form-group">
                        <label for="api_key">Google Maps API Key:</label>
                        <input type="text" id="api_key" name="api_key" value="{{ api_key }}" required>
                    </div>
                    <button type="submit" class="btn">Update API Key</button>
                </form>
            </div>
            
            <div class="card">
                <h2>Your Routes</h2>
                {% if routes %}
                <table>
                    <thead>
                        <tr>
                            <th>Source</th>
                            <th>Destination</th>
                            <th>Current Estimate</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for route in routes %}
                        <tr>
                            <td>
                                <strong>{{ route.source_name }}</strong><br>
                                <small>{{ route.source_address }}</small>
                            </td>
                            <td>
                                <strong>{{ route.destination_name }}</strong><br>
                                <small>{{ route.destination_address }}</small>
                            </td>
                            <td>
                                {% if route.duration != "N/A" %}
                                {{ route.duration }} min
                                {% else %}
                                N/A
                                {% endif %}
                            </td>
                            <td>
                                <form action="/remove-route" method="post">
                                    <input type="hidden" name="source_address" value="{{ route.source_address }}">
                                    <input type="hidden" name="destination_address" value="{{ route.destination_address }}">
                                    <button type="submit" class="btn-delete">Remove</button>
                                </form>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p>No routes added yet. Add your first route below.</p>
                {% endif %}
            </div>
            
            <div class="card">
                <h2>Add New Route</h2>
                <form action="/add-route" method="post">
                    <div class="form-group">
                        <label for="source_name">Source Name:</label>
                        <input type="text" id="source_name" name="source_name" required placeholder="Home, Work, etc.">
                    </div>
                    <div class="form-group">
                        <label for="source_address">Source Address:</label>
                        <input type="text" id="source_address" name="source_address" required placeholder="Full address">
                    </div>
                    <div class="form-group">
                        <label for="destination_name">Destination Name:</label>
                        <input type="text" id="destination_name" name="destination_name" required placeholder="Home, Work, etc.">
                    </div>
                    <div class="form-group">
                        <label for="destination_address">Destination Address:</label>
                        <input type="text" id="destination_address" name="destination_address" required placeholder="Full address">
                    </div>
                    <button type="submit" class="btn">Add Route</button>
                </form>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(os.path.join(templates_dir, "index.html"), "w") as f:
        f.write(index_html)
    
   
    css_content = """
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: Arial, sans-serif;
    }
    
    body {
        background-color: #f5f5f5;
        color: #333;
        line-height: 1.6;
    }
    
    .container {
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
    }
    
    h1 {
        text-align: center;
        margin-bottom: 20px;
        color: #2c3e50;
    }
    
    h2 {
        color: #3498db;
        margin-bottom: 15px;
    }
    
    .card {
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin-bottom: 20px;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
    }
    
    table th, table td {
        padding: 12px 15px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }
    
    table th {
        background-color: #f8f9fa;
        font-weight: bold;
    }
    
    form {
        display: flex;
        flex-direction: column;
    }
    
    .form-group {
        margin-bottom: 15px;
    }
    
    label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
    }
    
    input[type="text"] {
        width: 100%;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 14px;
    }
    
    .btn, .btn-delete {
        padding: 10px 15px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
    }
    
    .btn {
        background-color: #3498db;
        color: white;
    }
    
    .btn:hover {
        background-color: #2980b9;
    }
    
    .btn-delete {
        background-color: #e74c3c;
        color: white;
    }
    
    .btn-delete:hover {
        background-color: #c0392b;
    }
    """
    
    with open(os.path.join(static_dir, "styles.css"), "w") as f:
        f.write(css_content)

create_template_files()

def main():
    print("Starting Route Monitor UI...")
    print(f"Open your browser and navigate to http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()