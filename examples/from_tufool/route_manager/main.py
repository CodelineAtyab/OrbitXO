from pathlib import Path
from typing import List, Dict, Any
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, constr, ValidationError
import json

app = FastAPI(title="Route Manager")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

CONFIG_PATH = Path("config.json")

# ---------- Utilities ----------
def load_config() -> Dict[str, Any]:
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(json.dumps({"routes": []}, indent=2, ensure_ascii=False), encoding="utf-8")
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_config(data: Dict[str, Any]) -> None:
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def is_duplicate(new_route: Dict[str, str], existing: List[Dict[str, str]]) -> bool:
    def norm(x: str) -> str:
        return " ".join(x.strip().lower().split())
    for r in existing:
        if (
            norm(r["source_name"]) == norm(new_route["source_name"]) and
            norm(r["source_address"]) == norm(new_route["source_address"]) and
            norm(r["destination_name"]) == norm(new_route["destination_name"]) and
            norm(r["destination_address"]) == norm(new_route["destination_address"])
        ):
            return True
    return False

# ---------- Validation Model ----------
class RouteIn(BaseModel):
    source_name: constr(strip_whitespace=True, min_length=2, max_length=50)
    source_address: constr(strip_whitespace=True, min_length=5, max_length=255)
    destination_name: constr(strip_whitespace=True, min_length=2, max_length=50)
    destination_address: constr(strip_whitespace=True, min_length=5, max_length=255)

    # Super simple "address-like" check: require a space and either a comma or a digit
    # to avoid obviously invalid inputs like "x" or "----".
    @staticmethod
    def looks_addressy(s: str) -> bool:
        s = s.strip()
        return (" " in s) and ("," in s or any(ch.isdigit() for ch in s))

    def validate_addresses(self):
        errors = {}
        if not self.looks_addressy(self.source_address):
            errors["source_address"] = "Please enter a realistic address (include spaces and preferably a street/area)."
        if not self.looks_addressy(self.destination_address):
            errors["destination_address"] = "Please enter a realistic address (include spaces and preferably a street/area)."
        return errors

# ---------- Routes ----------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request, added: int | None = None, deleted: int | None = None, error: str | None = None):
    cfg = load_config()
    routes = list(enumerate(cfg.get("routes", [])))  # [(idx, route), ...]
    messages = []
    if added:
        messages.append({"type": "success", "text": "New route added."})
    if deleted:
        messages.append({"type": "success", "text": "Route removed."})
    if error:
        messages.append({"type": "error", "text": error})
    return templates.TemplateResponse("index.html", {"request": request, "routes": routes, "messages": messages})

@app.post("/add")
async def add_route(
    source_name: str = Form(...),
    source_address: str = Form(...),
    destination_name: str = Form(...),
    destination_address: str = Form(...),
):
    cfg = load_config()
    try:
        route_in = RouteIn(
            source_name=source_name,
            source_address=source_address,
            destination_name=destination_name,
            destination_address=destination_address,
        )
    except ValidationError as e:
        # Return first error as a simple flash message
        err_msg = e.errors()[0].get("msg", "Invalid input.")
        return RedirectResponse(url=f"/?error={err_msg}", status_code=303)

    # Custom address checks
    addr_errors = route_in.validate_addresses()
    if addr_errors:
        # Prefer returning destination error first if present
        err_msg = addr_errors.get("source_address") or addr_errors.get("destination_address") or "Invalid addresses."
        return RedirectResponse(url=f"/?error={err_msg}", status_code=303)

    new_route = route_in.model_dump()

    # Duplicate check
    if is_duplicate(new_route, cfg.get("routes", [])):
        return RedirectResponse(url="/?error=That route already exists.", status_code=303)

    cfg["routes"].append(new_route)
    save_config(cfg)
    return RedirectResponse(url="/?added=1", status_code=303)

@app.post("/delete/{idx}")
async def delete_route(idx: int):
    cfg = load_config()
    routes = cfg.get("routes", [])
    if idx < 0 or idx >= len(routes):
        return RedirectResponse(url="/?error=Invalid route index.", status_code=303)
    routes.pop(idx)
    cfg["routes"] = routes
    save_config(cfg)
    return RedirectResponse(url="/?deleted=1", status_code=303)

# Small JSON API for debugging or reuse
@app.get("/api/routes")
async def api_routes():
    return JSONResponse(load_config())
