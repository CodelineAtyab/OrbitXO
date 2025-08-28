import os, json, uuid, requests
from datetime import datetime
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
app = FastAPI(title="Routes UI")
CONFIG_PATH = "routes_config.json"
TEMPLATES = Jinja2Templates(directory="templates")
API_KEY = os.getenv("MAPS_API_KEY") 
def load_config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump({"routes": []}, f)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
def fetch_estimate(origin, destination):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {"origin": origin, "destination": destination, "mode": "driving", "key": API_KEY}
    r = requests.get(url, params=params)
    data = r.json()
    if data.get("status") == "OK":
        leg = data["routes"][0]["legs"][0]
        return leg["duration"]["text"], leg["distance"]["text"], None
    return None, None, data.get("status")
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    cfg = load_config()
    for r in cfg["routes"]:
        duration, distance, err = fetch_estimate(r["source_address"], r["destination_address"])
        if duration:
            r["current_estimate"] = duration
            r["current_distance"] = distance
            r["updated_at"] = datetime.utcnow().isoformat(timespec="seconds")
            r["last_error"] = None
        else:
            r["last_error"] = err
    save_config(cfg)
    return TEMPLATES.TemplateResponse("index.html", {"request": request, "routes": cfg["routes"]})
@app.post("/add")
async def add_route(source_name: str = Form(...), source_address: str = Form(...),
                    destination_name: str = Form(...), destination_address: str = Form(...)):
    cfg = load_config()
    cfg["routes"].append({
        "id": str(uuid.uuid4()),
        "source_name": source_name, "source_address": source_address,
        "destination_name": destination_name, "destination_address": destination_address
    })
    save_config(cfg)
    return RedirectResponse("/", status_code=303)
@app.get("/remove")
async def remove_route(id: str):
    cfg = load_config()
    cfg["routes"] = [r for r in cfg["routes"] if r["id"] != id]
    save_config(cfg)
    return RedirectResponse("/", status_code=303)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("ui:app", host="127.0.0.1", port=8000, reload=True)