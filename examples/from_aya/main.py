from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import os
from typing import List, Dict, Any
from pydantic import BaseModel, field_validator
import uvicorn

app = FastAPI(title="Route Manager", description="Manage your source-destination pairs")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Configuration file path
CONFIG_FILE = "routes_config.json"

# Data models
class RouteConfig(BaseModel):
    source_name: str
    source_address: str
    destination_name: str
    destination_address: str
    
    @field_validator('source_name', 'destination_name')
    @classmethod
    def validate_names(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip()
    
    @field_validator('source_address', 'destination_address')
    @classmethod
    def validate_addresses(cls, v):
        if not v or len(v.strip()) < 10:
            raise ValueError('Address must be at least 10 characters long')
        return v.strip()

# Utility functions
def load_config() -> Dict[str, Any]:
    """Load configuration from JSON file"""
    if not os.path.exists(CONFIG_FILE):
        # Create default config if file doesn't exist
        default_config = {
            "routes": [
                {
                    "source_name": "Home",
                    "source_address": "123 Main Street, City, Country",
                    "destination_name": "Work",
                    "destination_address": "456 Business Ave, City, Country"
                },
                {
                    "source_name": "Home",
                    "source_address": "123 Main Street, City, Country",
                    "destination_name": "Gym",
                    "destination_address": "789 Fitness Road, City, Country"
                }
            ]
        }
        save_config(default_config)
        return default_config
    
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"routes": []}

def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to JSON file"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def get_route_estimate(source: str, destination: str) -> str:
    """Mock function to get route time estimate"""
    # In a real application, this would call a mapping API
    import random
    time = random.randint(5, 45)
    return f"{time} min"

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Display main page with routes table"""
    config = load_config()
    routes = config.get("routes", [])
    
    # Add time estimates to routes
    for route in routes:
        route["estimate"] = get_route_estimate(
            route["source_address"], 
            route["destination_address"]
        )
    
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "routes": routes}
    )

@app.post("/add_route")
async def add_route(
    source_name: str = Form(...),
    source_address: str = Form(...),
    destination_name: str = Form(...),
    destination_address: str = Form(...)
):
    """Add a new route"""
    try:
        # Validate input
        route = RouteConfig(
            source_name=source_name,
            source_address=source_address,
            destination_name=destination_name,
            destination_address=destination_address
        )
        
        # Load current config
        config = load_config()
        
        # Add new route
        config["routes"].append(route.model_dump())
        
        # Save updated config
        save_config(config)
        
        return RedirectResponse(url="/", status_code=303)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/remove_route/{route_index}")
async def remove_route(route_index: int):
    """Remove a route by index"""
    config = load_config()
    routes = config.get("routes", [])
    
    if 0 <= route_index < len(routes):
        routes.pop(route_index)
        save_config(config)
    
    return RedirectResponse(url="/", status_code=303)

@app.get("/api/routes")
async def get_routes():
    """API endpoint to get all routes"""
    config = load_config()
    return config.get("routes", [])

# Create templates directory and HTML template
def create_template():
    """Create the HTML template file"""
    os.makedirs("templates", exist_ok=True)
    
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Route Manager</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            color: #333;
        }
        .container {
            display: grid;
            gap: 30px;
        }
        .routes-section, .add-section {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .section-title {
            color: #444;
            margin-bottom: 20px;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }
        .routes-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        .routes-table th, .routes-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        .routes-table th {
            background-color: #f8f9fa;
            font-weight: 600;
            color: #555;
        }
        .routes-table tr:hover {
            background-color: #f8f9fa;
        }
        .route-info {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        .route-name {
            font-weight: 600;
            color: #333;
        }
        .route-address {
            color: #666;
            font-size: 0.9em;
        }
        .estimate {
            background-color: #e7f3ff;
            color: #0066cc;
            padding: 4px 8px;
            border-radius: 15px;
            font-size: 0.9em;
            font-weight: 500;
            text-align: center;
        }
        .remove-btn {
            background-color: #dc3545;
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9em;
            transition: background-color 0.2s;
        }
        .remove-btn:hover {
            background-color: #c82333;
        }
        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .form-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        .form-group label {
            font-weight: 600;
            color: #555;
        }
        .form-group input {
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 1em;
            transition: border-color 0.2s;
        }
        .form-group input:focus {
            outline: none;
            border-color: #007bff;
        }
        .submit-btn {
            grid-column: 1 / -1;
            background-color: #28a745;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            transition: background-color 0.2s;
        }
        .submit-btn:hover {
            background-color: #218838;
        }
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        .arrow {
            color: #007bff;
            font-weight: bold;
        }
        @media (max-width: 768px) {
            .form-grid {
                grid-template-columns: 1fr;
            }
            .routes-table {
                font-size: 0.9em;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🗺️ Route Manager</h1>
        <p>Manage your source-destination pairs and monitor travel times</p>
    </div>

    <div class="container">
        <div class="routes-section">
            <h2 class="section-title">Current Routes</h2>
            {% if routes %}
            <table class="routes-table">
                <thead>
                    <tr>
                        <th>Route</th>
                        <th>Current Estimate</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {% for route in routes %}
                    <tr>
                        <td>
                            <div class="route-info">
                                <div class="route-name">
                                    {{ route.source_name }} <span class="arrow">→</span> {{ route.destination_name }}
                                </div>
                                <div class="route-address">
                                    From: {{ route.source_address }}
                                </div>
                                <div class="route-address">
                                    To: {{ route.destination_address }}
                                </div>
                            </div>
                        </td>
                        <td>
                            <span class="estimate">{{ route.estimate }}</span>
                        </td>
                        <td>
                            <form method="post" action="/remove_route/{{ loop.index0 }}" style="display: inline;">
                                <button type="submit" class="remove-btn" 
                                        onclick="return confirm('Are you sure you want to remove this route?')">
                                    Remove
                                </button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            {% else %}
            <div class="empty-state">
                <p>No routes configured yet. Add your first route below!</p>
            </div>
            {% endif %}
        </div>

        <div class="add-section">
            <h2 class="section-title">Add New Route</h2>
            <form method="post" action="/add_route">
                <div class="form-grid">
                    <div class="form-group">
                        <label for="source_name">Source Name:</label>
                        <input type="text" id="source_name" name="source_name" 
                               placeholder="e.g., Home, Office" required>
                    </div>
                    <div class="form-group">
                        <label for="destination_name">Destination Name:</label>
                        <input type="text" id="destination_name" name="destination_name" 
                               placeholder="e.g., Work, Gym" required>
                    </div>
                    <div class="form-group">
                        <label for="source_address">Source Address:</label>
                        <input type="text" id="source_address" name="source_address" 
                               placeholder="123 Main Street, City, Country" required>
                    </div>
                    <div class="form-group">
                        <label for="destination_address">Destination Address:</label>
                        <input type="text" id="destination_address" name="destination_address" 
                               placeholder="456 Business Ave, City, Country" required>
                    </div>
                    <button type="submit" class="submit-btn">Add Route</button>
                </div>
            </form>
        </div>
    </div>
</body>
</html>'''
    
    with open("templates/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    # Create template file
    create_template()
    
    # Run the application
    print("Starting Route Manager...")
    print("Creating templates directory...")
    print("Server will be available at: http://127.0.0.1:8000")
    
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)