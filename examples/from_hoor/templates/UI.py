from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
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

# ----------------------------
# HTML Dashboard
# ----------------------------
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Route Manager Dashboard</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background:#f5f7fa; color:#333; }
.container { max-width:1200px; margin:0 auto; padding:20px; }
h1 { text-align:center; margin-bottom:30px; }
.routes-table { width:100%; border-collapse:collapse; }
.routes-table th, .routes-table td { padding:12px; text-align:left; border-bottom:1px solid #ddd; }
.routes-table th { background-color:#3498db; color:white; }
.route-info { font-weight:500; }
.estimate { color:#27ae60; font-weight:600; }
.remove-btn { background-color:#e74c3c; color:white; border:none; padding:6px 12px; border-radius:4px; cursor:pointer; }
.remove-btn:hover { background-color:#c0392b; }
.add-form { background:white; padding:20px; border-radius:10px; margin-top:30px; }
.form-group { margin-bottom:15px; }
.form-group label { font-weight:600; }
.form-group input { width:100%; padding:8px; border-radius:4px; border:1px solid #ccc; }
.submit-btn { background-color:#3498db; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer; }
.submit-btn:hover { background-color:#2980b9; }
.alert { padding:10px; margin-bottom:15px; border-radius:5px; }
.alert-success { background:#d4edda; color:#155724; }
.alert-error { background:#f8d7da; color:#721c24; }
.empty-state { text-align:center; font-style:italic; padding:20px; color:#7f8c8d; }
</style>
</head>
<body>
<div class="container">
<h1>🗺️ Route Manager</h1>
<div id="alert-container"></div>
<table class="routes-table">
<thead>
<tr><th>Route</th><th>Estimated Time</th><th>Action</th></tr>
</thead>
<tbody id="routes-tbody">
<tr><td colspan="3" class="empty-state">Loading routes...</td></tr>
</tbody>
</table>

<div class="add-form">
<h2>Add New Route</h2>
<div class="form-group">
<label>Source Name</label>
<input type="text" id="source_name">
</div>
<div class="form-group">
<label>Source Address</label>
<input type="text" id="source_address">
</div>
<div class="form-group">
<label>Destination Name</label>
<input type="text" id="destination_name">
</div>
<div class="form-group">
<label>Destination Address</label>
<input type="text" id="destination_address">
</div>
<button class="submit-btn" onclick="addRoute()">Add Route</button>
</div>
</div>

<script>
function showAlert(msg, type='success') {
    const container = document.getElementById('alert-container');
    const div = document.createElement('div');
    div.className = 'alert alert-' + type;
    div.textContent = msg;
    container.appendChild(div);
    setTimeout(()=>div.remove(), 4000);
}

async function loadRoutes() {
    try {
        const res = await fetch('/routes');
        const data = await res.json();
        const tbody = document.getElementById('routes-tbody');
        if(!data.routes || data.routes.length==0){
            tbody.innerHTML='<tr><td colspan="3" class="empty-state">No routes yet</td></tr>';
            return;
        }
        tbody.innerHTML = data.routes.map(r=>`
            <tr>
            <td>${r.source_name} → ${r.destination_name}<br><small>${r.source_address} → ${r.destination_address}</small></td>
            <td class="estimate">${r.estimated_time_minutes}</td>
            <td><button class="remove-btn" onclick="removeRoute('${r.source_address}','${r.destination_address}')">Remove</button></td>
            </tr>`).join('');
    } catch(e){ showAlert('Error loading routes','error'); }
}

async function addRoute(){
    const payload={
        source_name: document.getElementById('source_name').value,
        source_address: document.getElementById('source_address').value,
        destination_name: document.getElementById('destination_name').value,
        destination_address: document.getElementById('destination_address').value
    };
    try {
        const res = await fetch('/routes', {
            method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)
        });
        if(res.ok){ showAlert('Route added'); loadRoutes(); }
        else { showAlert('Error adding route','error'); }
    } catch(e){ showAlert('Error adding route','error'); }
}

async function removeRoute(source,dest){
    const routes = await fetch('/routes').then(r=>r.json());
    const index = routes.routes.findIndex(r=>r.source_address==source && r.destination_address==dest);
    if(index==-1){ showAlert('Route not found','error'); return; }
    const all_routes = routes.routes;
    all_routes.splice(index,1);
    await fetch('/routes', {method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify(all_routes)});
    showAlert('Route removed'); loadRoutes();
}

document.addEventListener('DOMContentLoaded', loadRoutes);
</script>
</body>
</html>
"""

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
    def not_empty(cls,v):
        if not v or not v.strip(): raise ValueError('Field cannot be empty')
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
                with open(self.file,'r') as f:
                    self.config=json.load(f)
                    return
            except:
                pass
        self.config=DEFAULT_CONFIG.copy()
        self.save()

    def save(self):
        with open(self.file,'w') as f:
            json.dump(self.config,f,indent=2,ensure_ascii=False)

    def get_routes(self):
        return self.config.get("routes", [])

    async def update_estimates(self):
        for r in self.get_routes():
            r['estimated_time_minutes']=await self.fetch_time(r['source_address'],r['destination_address'])
        self.save()

    async def fetch_time(self,origin,dest):
        if not MAPS_API_KEY: return "API key missing"
        url="https://maps.googleapis.com/maps/api/distancematrix/json"
        params={"origins":origin,"destinations":dest,"key":MAPS_API_KEY,"units":"metric","departure_time":"now","traffic_model":"best_guess"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url,params=params) as r:
                    data = await r.json()
                    elem = data.get("rows",[{}])[0].get("elements",[{}])[0]
                    if elem.get("status")=="OK":
                        if "duration_in_traffic" in elem: return elem["duration_in_traffic"]["text"]
                        if "duration" in elem: return elem["duration"]["text"]
                    return "No estimate"
        except: return "Error"

manager = Manager(CONFIG_FILE)

# ----------------------------
# API Endpoints
# ----------------------------
@app.get("/", response_class=HTMLResponse)
async def dashboard(): return HTML_PAGE

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
async def update_routes(routes:list):
    manager.config['routes'] = routes
    manager.save()
    return {"status":"ok"}

@app.get("/routes.json")
async def download_json():
    return FileResponse(CONFIG_FILE, media_type="application/json", filename="routes_config.json")

# ----------------------------
# Auto open JSON in browser
# ----------------------------
def _open_browser(): webbrowser.open_new_tab("http://127.0.0.1:8000/routes.json")

if __name__=="__main__":
    threading.Timer(1.2,_open_browser).start()
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)
