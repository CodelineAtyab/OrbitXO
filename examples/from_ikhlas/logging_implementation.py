import requests
import dotenv
import json
import os
import logging 
import logging.config
from logging.handlers import TimedRotatingFileHandler

# Configure the logging
logfile="applog.log"
log_configuration={
    "version":1,
    "disable_existing_loggers":False,
    "formatters":{
        "standard":{
            "format":"%(asctime)s %(levelname)s [%(module)s:%(lineno)d] %(message)s",
            "datefmt":"%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers":{
        "console":{
            "class":"logging.StreamHandler",
            "level":"DEBUG",
            "formatter":"standard",
            "stream":"ext://sys.stdout",
        },
        "file":{
            "class":"logging.handlers.TimedRotatingFileHandler",
            "level":"DEBUG",
            "formatter":"standard",
            "filename":logfile,
            "when":"D",
            "interval":1,
            "backupCount":7,
            "encoding":"utf-8",
        },
    },
    "root":{
        "level":"DEBUG",
        "handlers":["console","file"]
    },
}
logging.config.dictConfig(log_configuration)
logger=logging.getLogger(__name__)

#Google API calling
def route_information():
    dotenv.load_dotenv()
    API_KEY=os.getenv("GOOGLE_MAPS_API_KEY")
    url="https://routes.googleapis.com/directions/v2:computeRoutes"
    headers={"content-type":"application/json",
             "X-Goog-Api-Key":API_KEY,
             "X-Goog-FieldMask":"routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"}
    
    body={
        "origin":{"address":"Muscat Private Hospital, Muscat, Oman"},
        "destination":{"address":"Codeline, Muscat, Oman"},
        "travelMode":"DRIVE",
        "routingPreference":"TRAFFIC_AWARE",
        "computeAlternativeRoutes":False,
        "routeModifiers":{
            "avoidTolls":False,
            "avoidHighways":False,
            "avoidFerries":False
        },
        "languageCode":"en-US",
        "units":"METRIC"
    }
    logger.info("Sendeing request to Google API")
    logger.debug("Body request:%s",body)


    try:
     response = requests.post(url, headers=headers, data=json.dumps(body))
    except requests.RequestException as e:
        logger.error("Request failed: %s", e)
        return

    if response.ok:
        data=response.json()
        route=data["routes"][0]
        duration_seconds=int(route["duration"].rstrip("s"))
        duration_minutes=duration_seconds/60 #in min
        distance_km=route["distanceMeters"]/1000 #in km

        logger.info("API called successfully")
        logger.info("Estimated travel time: %.1f minutes",duration_minutes)
        logger.info("Distance: %.2f km",distance_km)

        return (duration_minutes,distance_km)
    else:
        logger.error("Error response %s: %s", response.status_code, response.text)
        return None


if __name__=="__main__":
    result=route_information()
    if result:
        duration,distance = result
        print(f"Travel time: {duration:.1f} minutes")
        print(f"Distance: {distance:.2f} km")