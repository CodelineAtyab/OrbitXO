from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, field_validator
from datetime import datetime
import os, json, asyncio, aiohttp, threading, webbrowser

# ----------------------------
# Environment & Files
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "routes_config.json")
MAPS_API_KEY = os.getenv("MAPS_API_KEY")

# Default JSON structure
DEFAULT_CONFIG = {
    "routes": [],
    "settings": {"created_at": datetime.now().isoformat(), "version": "1.0.0"}
}

# ----------------------------
# Initialize JSON file
# ----------------------------
def initialize_json():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)

initialize_json()

# ----------------------------
# FastAPI App
# ----------------------------
app = FastAPI(title="Route Manager", version="1.0.0")

# Mount static files (for serving HTML, CSS, JS files)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ----------------------------
# Pydantic Model
# ----------------------------
class RouteModel(BaseModel):
    source_name: str
    source_address: str
    destination_name: str
    destination_address: str
    estimated_time_minutes: str = "Calculating..."

    @field_validator('*')
    @classmethod
    def not_empty(cls, v):
        if not v or not v.strip(): 
            raise ValueError('Field cannot be empty')
        return v.strip()

# ----------------------------
# Route Manager
# ----------------------------
class Manager:
    def __init__(self, file):
        self.file = file
        self.load()

    def load(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, 'r') as f:
                    self.config = json.load(f)
                    return
            except:
                pass
        self.config = DEFAULT_CONFIG.copy()
        self.save()

    def save(self):
        with open(self.file, 'w') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def get_routes(self):
        return self.config.get("routes", [])

    async def update_estimates(self):
        for r in self.get_routes():
            r['estimated_time_minutes'] = await self.fetch_time(r['source_address'], r['destination_address'])
        self.save()

    async def fetch_time(self, origin, dest):
        if not MAPS_API_KEY: 
            return "API key missing"
        
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": origin,
            "destinations": dest,
            "key": MAPS_API_KEY,
            "units": "metric",
            "departure_time": "now",
            "traffic_model": "best_guess"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as r:
                    data = await r.json()
                    elem = data.get("rows", [{}])[0].get("elements", [{}])[0]
                    if elem.get("status") == "OK":
                        if "duration_in_traffic" in elem: 
                            return elem["duration_in_traffic"]["text"]
                        if "duration" in elem: 
                            return elem["duration"]["text"]
                    return "No estimate"
        except: 
            return "Error"

manager = Manager(CONFIG_FILE)

# ----------------------------
# API Endpoints
# ----------------------------
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    # Serve the HTML file from static directory
    return FileResponse('static/index.html')

@app.get("/routes")
async def list_routes():
    await manager.update_estimates()
    return {"routes": manager.get_routes()}

@app.post("/routes")
async def add_route(route: RouteModel):
    routes = manager.get_routes()
    routes.append(route.dict())
    manager.config['routes'] = routes
    manager.save()
    await manager.update_estimates()
    return route.dict()

@app.put("/routes")
async def update_routes(routes: list):
    manager.config['routes'] = routes
    manager.save()
    return {"status": "ok"}

@app.get("/routes.json")
async def download_json():
    return FileResponse(CONFIG_FILE, media_type="application/json", filename="routes_config.json")

# ----------------------------
# Auto open browser
# ----------------------------
def _open_browser(): 
    webbrowser.open_new_tab("http://127.0.0.1:8000")

if __name__ == "__main__":
    # Create static directory if it doesn't exist
    os.makedirs("static", exist_ok=True)
    
    threading.Timer(1.2, _open_browser).start()
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)