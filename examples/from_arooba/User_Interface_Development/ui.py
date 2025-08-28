# user_interface.py
# Simple Routes UI (view/add/remove) + live Estimate (min & km)
# Uses Google Distance Matrix if MAPS_API_KEY exists, otherwise OpenStreetMap (Nominatim + OSRM).
# Includes in-page diagnostics and /debug endpoint.
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, field_validator
from typing import Optional, Tuple
from datetime import datetime, timedelta
import json, os, uuid, requests

APP_VERSION = "v3-osm-debug"

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

app = FastAPI(title=f"Routes UI ({APP_VERSION})")

CONFIG_PATH = "routes_config.json"
ESTIMATE_STALENESS_MIN = 10   # refresh if older than this (minutes)
OSM_UA = os.getenv("OSM_USER_AGENT", f"routes-ui/{APP_VERSION}")

def load_config() -> dict:
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump({"routes": []}, f, ensure_ascii=False, indent=2)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(cfg: dict) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

def maps_api_key() -> Optional[str]:
    return os.getenv("MAPS_API_KEY") or os.getenv("GOOGLE_MAPS_API_KEY")

class Route(BaseModel):
    id: str
    source_name: str
    source_address: str
    destination_name: str
    destination_address: str
    current_estimate_min: Optional[int] = None
    current_distance_km: Optional[float] = None
    updated_at: Optional[str] = None
    last_error: Optional[str] = None  # show reason if estimate fails

class RouteInput(BaseModel):
    source_name: str
    source_address: str
    destination_name: str
    destination_address: str

    @field_validator("source_name", "destination_name")
    @classmethod
    def validate_names(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Name is required.")
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Name is too short.")
        return v

    @field_validator("source_address", "destination_address")
    @classmethod
    def validate_addresses(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Address is required.")
        v = v.strip()
        if len(v) < 5:
            raise ValueError("Address is too short.")
        return v

# ---------- Google Distance Matrix ----------
def fetch_estimate_google(origin: str, destination: str) -> Tuple[Optional[Tuple[int, float]], Optional[str]]:
    key = maps_api_key()
    if not key:
        return None, "NO_GOOGLE_KEY"
    try:
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {"origins": origin, "destinations": destination, "mode": "driving", "units": "metric", "key": key}
        r = requests.get(url, params=params, timeout=12)
        data = r.json()
        if data.get("status") != "OK":
            return None, f"GOOGLE_STATUS:{data.get('status')}"
        rows = data.get("rows", [])
        if not rows or not rows[0].get("elements"):
            return None, "GOOGLE_EMPTY_ROWS"
        el = rows[0]["elements"][0]
        if el.get("status") != "OK":
            return None, f"GOOGLE_ELEMENT:{el.get('status')}"
        sec = el["duration"]["value"]
        meters = el["distance"]["value"]
        minutes = int(round(sec / 60))
        km = round(meters / 1000.0, 1)
        return (minutes, km), None
    except Exception as e:
        return None, f"GOOGLE_ERROR:{type(e).__name__}"

# ---------- OpenStreetMap (fallback, no key) ----------
def geocode_osm(query: str) -> Tuple[Optional[Tuple[float, float]], Optional[str]]:
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": query, "format": "json", "limit": 1}
        r = requests.get(url, params=params, headers={"User-Agent": OSM_UA}, timeout=15)
        arr = r.json()
        if not arr:
            return None, "OSM_GEOCODE_EMPTY"
        return (float(arr[0]["lat"]), float(arr[0]["lon"])), None
    except Exception as e:
        return None, f"OSM_GEOCODE_ERR:{type(e).__name__}"

def fetch_estimate_osm(origin_addr: str, dest_addr: str) -> Tuple[Optional[Tuple[int, float]], Optional[str]]:
    o, e1 = geocode_osm(origin_addr)
    if not o:
        return None, e1
    d, e2 = geocode_osm(dest_addr)
    if not d:
        return None, e2
    try:
        url = f"https://router.project-osrm.org/route/v1/driving/{o[1]},{o[0]};{d[1]},{d[0]}"
        params = {"overview": "false"}
        r = requests.get(url, params=params, headers={"User-Agent": OSM_UA}, timeout=15)
        data = r.json()
        if data.get("code") != "Ok" or not data.get("routes"):
            return None, f"OSRM_CODE:{data.get('code')}"
        route = data["routes"][0]
        km = round(route["distance"] / 1000.0, 1)
        minutes = int(round(route["duration"] / 60))
        return (minutes, km), None
    except Exception as e:
        return None, f"OSRM_ERR:{type(e).__name__}"

def fetch_estimate(origin: str, destination: str) -> Tuple[Optional[Tuple[int, float]], Optional[str], str]:
    # Try Google first; if no key/failed, fallback to OSM
    res, err = fetch_estimate_google(origin, destination)
    if res is not None:
        return res, None, "google"
    res2, err2 = fetch_estimate_osm(origin, destination)
    if res2 is not None:
        return res2, None, "osm"
    # both failed
    return None, (err or err2 or "UNKNOWN_ERROR"), "none"

def refresh_estimates_if_needed(cfg: dict) -> bool:
    changed = False
    now = datetime.utcnow()
    for r in cfg.get("routes", []):
        stale = True
        if r.get("updated_at"):
            try:
                last = datetime.fromisoformat(r["updated_at"])
                stale = (now - last) > timedelta(minutes=ESTIMATE_STALENESS_MIN)
            except Exception:
                stale = True
        if r.get("current_estimate_min") is None or r.get("current_distance_km") is None or stale:
            res, err, provider = fetch_estimate(r["source_address"], r["destination_address"])
            if res is not None:
                minutes, km = res
                r["current_estimate_min"] = minutes
                r["current_distance_km"] = float(km)
                r["updated_at"] = now.isoformat(timespec="seconds")
                r["last_error"] = None
                r["provider"] = provider
                changed = True
            else:
                r["last_error"] = err
                r["provider"] = provider
                changed = True
    return changed

# ---------- UI ----------
BASE_CSS = """
<style>
:root { font-family: 'Segoe UI', Roboto, Arial, sans-serif; }

body {
  max-width: 1000px;
  margin: 32px auto;
  padding: 0 20px;
  background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
  animation: fadeIn 1.2s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

h1 {
  margin-bottom: 10px;
  color: #4a148c;
  font-size: 28px;
  text-align: center;
  animation: glow 2s ease-in-out infinite alternate;
}
@keyframes glow {
  from { text-shadow: 0 0 5px #b39ddb; }
  to { text-shadow: 0 0 20px #7e57c2; }
}

.card {
  border: none;
  border-radius: 16px;
  padding: 20px;
  margin-top: 20px;
  background: #fff;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  transition: transform 0.2s ease;
}
.card:hover {
  transform: translateY(-4px);
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 12px;
}
th, td {
  padding: 12px 10px;
  border-bottom: 1px solid #f1f1f1;
  text-align: left;
}
th {
  background: #f3e5f5;
  color: #4a148c;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
tr:hover {
  background-color: #fafafa;
  transition: background 0.3s ease;
}

.badge {
  display:inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  background: linear-gradient(135deg, #7e57c2, #5e35b1);
  color: white;
  font-size: 12px;
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(126,87,194,0.4); }
  70% { box-shadow: 0 0 0 10px rgba(126,87,194,0); }
  100% { box-shadow: 0 0 0 0 rgba(126,87,194,0); }
}

.btn {
  display:inline-block;
  padding: 10px 16px;
  border-radius: 8px;
  border: none;
  background: linear-gradient(135deg, #ab47bc, #7b1fa2);
  color: white;
  cursor: pointer;
  text-decoration:none;
  transition: transform 0.2s, background 0.3s;
}
.btn:hover {
  background: linear-gradient(135deg, #8e24aa, #6a1b9a);
  transform: scale(1.05);
}

.btn-danger {
  background: linear-gradient(135deg, #ef5350, #c62828);
}
.btn-danger:hover {
  background: linear-gradient(135deg, #e53935, #b71c1c);
}

.input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  transition: border-color 0.3s ease;
}
.input:focus {
  border-color: #7e57c2;
  outline: none;
  box-shadow: 0 0 6px rgba(126,87,194,0.4);
}

label {
  font-weight: 600;
  font-size: 14px;
  color: #4a148c;
}

.actions { display:flex; gap:10px; align-items:center; }

.footer {
  color:#777;
  font-size:12px;
  margin-top: 16px;
  text-align:center;
}
</style>
"""


def render_index(cfg: dict, error: Optional[str] = None, info: Optional[str] = None) -> str:
    key = maps_api_key()
    provider_banner = "" if key else '<div class="banner">No Google key — using OpenStreetMap fallback. (Version: %s)</div>' % APP_VERSION

    rows_html = ""
    for r in cfg.get("routes", []):
        estimate = "—"
        extra = ""
        if r.get("current_estimate_min") is not None and r.get("current_distance_km") is not None:
            estimate = f'{r["current_estimate_min"]} min • {r["current_distance_km"]} km'
            if r.get("updated_at"):
                extra += f'<br><small class="note">Updated: {r["updated_at"]}Z • Provider: {r.get("provider","?")}</small>'
        if r.get("last_error"):
            extra += f'<br><small class="err">Reason: {r["last_error"]}</small>'

        rows_html += f"""
        <tr>
            <td><span class="badge">{r["source_name"]}</span><br><small>{r["source_address"]}</small></td>
            <td>→</td>
            <td><span class="badge">{r["destination_name"]}</span><br><small>{r["destination_address"]}</small></td>
            <td>{estimate}{extra}</td>
            <td class="right">
                <a class="btn btn-danger" href="/remove?id={r['id']}" onclick="return confirm('Remove this route?');">Remove</a>
            </td>
        </tr>
        """

    error_html = f'<div class="card" style="border-color:#f3d1d1;background:#fff5f5;color:#b00020;"><b>Error:</b> {error}</div>' if error else ""
    info_html = f'<div class="card" style="border-color:#d1e7dd;background:#f1fff5;color:#0a6f37;"><b>Info:</b> {info}</div>' if info else ""

    return f"""
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8"/>
        <title>Routes UI</title>
        {BASE_CSS}
    </head>
    <body>
        <h1>Routes</h1>
        <small>View, add, and remove your source-destination pairs. (Version: {APP_VERSION})</small>
        {provider_banner}
        {error_html}{info_html}
        <div class="card">
            <div style="display:flex;align-items:center;justify-content:space-between;">
                <h3 style="margin:0 0 8px 0;">Current Routes</h3>
                <div class="actions">
                    <a class="btn" href="/refresh">Refresh Estimates</a>
                    <a class="btn" href="/debug" title="Diagnostics">Debug</a>
                </div>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Source</th>
                        <th></th>
                        <th>Destination</th>
                        <th>Estimate</th>
                        <th class="right">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html if rows_html else '<tr><td colspan="5"><i>No routes yet. Add your first route below.</i></td></tr>'}
                </tbody>
            </table>
        </div>
        <div class="card">
            <h3 style="margin:0 0 8px 0;">Add Route</h3>
            <form method="post" action="/add">
                <div class="grid">
                    <div>
                        <label>Source Name</label>
                        <input class="input" type="text" name="source_name" placeholder="Home" required>
                    </div>
                    <div>
                        <label>Destination Name</label>
                        <input class="input" type="text" name="destination_name" placeholder="Work" required>
                    </div>
                </div>
                <div class="grid" style="margin-top:10px;">
                    <div>
                        <label>Source Address</label>
                        <input class="input" type="text" name="source_address" placeholder="Muscat Grand Mall, Muscat, Oman" required>
                    </div>
                    <div>
                        <label>Destination Address</label>
                        <input class="input" type="text" name="destination_address" placeholder="Muscat International Airport, Muscat, Oman" required>
                    </div>
                </div>
                <div class="actions" style="margin-top:12px;">
                    <button class="btn" type="submit">Submit</button>
                    <a class="btn" href="/">Cancel</a>
                </div>
            </form>
            <hr>
            <div class="footer">
                If no Google key is set, estimates come from OpenStreetMap (approximate).
            </div>
        </div>
    </body>
    </html>
    """

# -------- Web routes --------
@app.get("/", response_class=HTMLResponse)
async def index():
    cfg = load_config()
    if refresh_estimates_if_needed(cfg):
        save_config(cfg)
    return render_index(cfg)

@app.get("/refresh", response_class=HTMLResponse)
async def refresh():
    cfg = load_config()
    if refresh_estimates_if_needed(cfg):
        save_config(cfg)
        msg = "Estimates refreshed."
    else:
        msg = "Nothing to refresh (check connectivity/addresses)."
    return HTMLResponse(render_index(cfg, info=msg))

@app.post("/add", response_class=HTMLResponse)
async def add_route(
    source_name: str = Form(...),
    source_address: str = Form(...),
    destination_name: str = Form(...),
    destination_address: str = Form(...)
):
    cfg = load_config()
    try:
        data = RouteInput(
            source_name=source_name,
            source_address=source_address,
            destination_name=destination_name,
            destination_address=destination_address,
        )
        new_route = Route(
            id=str(uuid.uuid4()),
            source_name=data.source_name,
            source_address=data.source_address,
            destination_name=data.destination_name,
            destination_address=data.destination_address,
        ).model_dump()
        # Try immediate estimate
        res, err, provider = fetch_estimate(new_route["source_address"], new_route["destination_address"])
        if res is not None:
            minutes, km = res
            new_route["current_estimate_min"] = minutes
            new_route["current_distance_km"] = float(km)
            new_route["updated_at"] = datetime.utcnow().isoformat(timespec="seconds")
            new_route["last_error"] = None
            new_route["provider"] = provider
        else:
            new_route["last_error"] = err
            new_route["provider"] = provider
        cfg["routes"].append(new_route)
        save_config(cfg)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        return HTMLResponse(render_index(cfg, error=str(e)), status_code=400)

@app.get("/remove")
async def remove_route(id: str):
    cfg = load_config()
    cfg["routes"] = [r for r in cfg.get("routes", []) if r.get("id") != id]
    save_config(cfg)
    return RedirectResponse(url="/", status_code=303)

# ---- Diagnostics ----
@app.get("/debug", response_class=PlainTextResponse)
def debug():
    # Quick runtime diagnostics
    key_state = bool(maps_api_key())
    # quick sample estimate using clear POIs in Muscat
    sample_o = "Muscat Grand Mall, Muscat, Oman"
    sample_d = "Muscat International Airport, Muscat, Oman"
    (res1, err1, prov1) = fetch_estimate(sample_o, sample_d)
    return (
        f"Version: {APP_VERSION}\n"
        f"Google key detected: {key_state}\n"
        f"Sample route: {sample_o} -> {sample_d}\n"
        f"Provider used: {prov1}\n"
        f"Estimate: {res1 if res1 else 'None'}\n"
        f"Error: {err1 if err1 else 'None'}\n"
    )

# Optional static
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("ui:app", host="127.0.0.1", port=8000, reload=True)