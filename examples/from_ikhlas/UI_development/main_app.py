from fastapi import FastAPI
from fastapi import Request
from fastapi import HTTPException
from fastapi import Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import json

app=FastAPI()

app.mount("/static",StaticFiles(directory="static"),name="static")
templates=Jinja2Templates(directory="templates")

config_file="config.json"

def load_route():
    if not os.path.exists(config_file):
        return[]
    with open(config_file,"r") as file:
        data=json.load(file)
    return data.get("routes",[])

def save_route(routes):
    with open(config_file,"w") as file:
        json.dump({"routes":routes},file, indent=2)

@app.get("/")
def home(request:Request):
    routes=load_route()
    return templates.TemplateResponse("index.html",{"request":request,"routes":routes})

#Adding route 
@app.post("/add")

def add_route(source_name: str = Form(...),
              source_address: str = Form(...),
              destination_name: str = Form(...),
              destination_address: str = Form(...)
              ):
    routes=load_route()

    if not source_name or not source_address or not destination_name or not destination_address:
        raise HTTPException(status_code=400,detail="All the fields are required")
    
    routes.append({"source_name": source_name,
                   "source_address": source_address,
                   "destination_name": destination_name,
                   "destination_address": destination_address})
    save_route(routes)
    return RedirectResponse("/",status_code=303)

#Remove route
@app.get("/remove")

def remove_route(index:int):
    routes=load_route()
    if 0 <= index < len(routes):
        routes.pop(index)
        save_route(routes)
    return RedirectResponse("/",status_code=303)