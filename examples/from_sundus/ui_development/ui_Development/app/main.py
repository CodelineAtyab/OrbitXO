from __future__ import annotations
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional
from .routes_repository import RoutesRepository
from .validation import validate_address_basic

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR.parent / "config" / "routes.json"

app = FastAPI(title="Routes UI")


# Static & templates
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Repository
repo = RoutesRepository(CONFIG_PATH)


class RouteIn(BaseModel):
    source_name: str = Field(min_length=1)
    source_address: str = Field(min_length=1)
    destination_name: str = Field(min_length=1)
    destination_address: str = Field(min_length=1)


@app.get("/")
def index(request: Request, error: Optional[str] = None):
    routes = repo.list_routes()
    return templates.TemplateResponse("index.html", {"request": request, "routes": routes, "error": error})


@app.post("/add")
def add_route(
    request: Request,
    source_name: str = Form(...),
    source_address: str = Form(...),
    destination_name: str = Form(...),
    destination_address: str = Form(...),
):
    # Pydantic field checks (non-empty)
    try:
        RouteIn(
            source_name=source_name,
            source_address=source_address,
            destination_name=destination_name,
            destination_address=destination_address,
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "routes": repo.list_routes(),
                "error": f"Invalid input: {e}"
            },
            status_code=400,
        )

    # Basic address validation
    ok_src, errs_src = validate_address_basic(source_address)
    ok_dst, errs_dst = validate_address_basic(destination_address)
    if not (ok_src and ok_dst):
        all_errs = errs_src + errs_dst
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "routes": repo.list_routes(),
                "error": " ".join(all_errs)
            },
            status_code=400,
        )

    repo.add_route(
        {
            "source_name": source_name.strip(),
            "source_address": source_address.strip(),
            "destination_name": destination_name.strip(),
            "destination_address": destination_address.strip(),
            "last_estimate_min": None,  # Optional: fill from your estimator later
        }
    )
    return RedirectResponse(url="/", status_code=303)


@app.post("/delete/{route_id}")
def delete_route(route_id: str):
    deleted = repo.delete_route(route_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Route not found")
    return RedirectResponse(url="/", status_code=303)
