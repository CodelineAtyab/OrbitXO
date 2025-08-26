import os
import json
import uvicorn
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import re
from typing import Optional
from datetime import datetime
from api import get_travel_time


app = FastAPI(title="Route Manager")

templates_dir = os.path.join(os.path.dirname(__file__), "templates")
static_dir = os.path.join(os.path.dirname(__file__), "static")

if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

templates = Jinja2Templates(directory=templates_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
TRAVEL_TIMES_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "travel_times.json")

def load_config():
    try:
        if not os.path.exists(CONFIG_FILE):
            default_config = {
                "source": "Muscat, Oman",
                "destination": "Sohar, Oman",
                "api_key": ""
            }
            with open(CONFIG_FILE, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config
        
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return {"source": "", "destination": "", "api_key": ""}

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def load_travel_times():
    try:
        if not os.path.exists(TRAVEL_TIMES_FILE):
            with open(TRAVEL_TIMES_FILE, 'w') as f:
                json.dump({}, f, indent=2)
            return {}
        
        with open(TRAVEL_TIMES_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading travel times: {e}")
        return {}

def save_travel_times(travel_times):
    try:
        with open(TRAVEL_TIMES_FILE, 'w') as f:
            json.dump(travel_times, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving travel times: {e}")
        return False

def create_route_key(source, destination):
    return f"{source.lower().replace(' ', '_')}_{destination.lower().replace(' ', '_')}"

def format_duration(minutes):
    hours = int(minutes // 60)
    remaining_minutes = int(minutes % 60)
    if hours > 0:
        if remaining_minutes > 0:
            return f"{hours} hour{'s' if hours > 1 else ''} {remaining_minutes} min"
        else:
            return f"{hours} hour{'s' if hours > 1 else ''}"
    else:
        return f"{remaining_minutes} min"

def validate_address(address):
    if not address or len(address) < 3:
        return False
    
    pattern = re.compile(r'^[a-zA-Z0-9\s,\.\-]+$')
    return bool(pattern.match(address))

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    travel_times = load_travel_times()
    
    routes = []
    for key, data in travel_times.items():
        source = data.get("source", "Unknown")
        destination = data.get("destination", "Unknown")
        duration_value = data.get("min_duration", 0)
        
        duration = format_duration(duration_value)
        
        routes.append({
            "key": key,
            "source": source,
            "destination": destination,
            "duration": duration,
            "duration_value": duration_value
        })
    
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "routes": routes}
    )

@app.post("/add-route")
async def add_route(
    source_name: str = Form(...),
    source_address: str = Form(...),
    destination_name: str = Form(...),
    destination_address: str = Form(...)
):
    if not validate_address(source_address) or not validate_address(destination_address):
        raise HTTPException(status_code=400, detail="Invalid address format")
    
    travel_times = load_travel_times()
    
    key = create_route_key(source_name, destination_name)
    
    if key in travel_times:
        raise HTTPException(status_code=400, detail="Route already exists")
    
    config = load_config()
    api_key = config.get("api_key", "")
    
    try:
        result = get_travel_time(source_address, destination_address, api_key)
        if not result["success"]:
            raise HTTPException(status_code=400, detail=f"Failed to get travel time: {result['error']}")
        
        duration_value = result["duration_value"] / 60  
        
        travel_times[key] = {
            "source": source_name,
            "destination": destination_name,
            "source_address": source_address,
            "destination_address": destination_address,
            "min_duration": duration_value,
            "recorded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "history": [
                {
                    "duration": duration_value,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            ]
        }
        
        if not save_travel_times(travel_times):
            raise HTTPException(status_code=500, detail="Failed to save travel times")
        
        return RedirectResponse(url="/", status_code=303)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/remove-route/{key}")
async def remove_route(key: str):
    travel_times = load_travel_times()
    
    if key not in travel_times:
        raise HTTPException(status_code=404, detail="Route not found")
    
    del travel_times[key]
    
    if not save_travel_times(travel_times):
        raise HTTPException(status_code=500, detail="Failed to save travel times")
    
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    css_dir = os.path.join(static_dir, "css")
    if not os.path.exists(css_dir):
        os.makedirs(css_dir)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
