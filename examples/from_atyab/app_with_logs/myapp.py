import requests
import logging
import json
import sys
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)

FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    handlers=[
        RotatingFileHandler(
            './logs/myapp.log',
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=7
        ),
        logging.StreamHandler(sys.stdout)
    ]
)

url = "https://aiops.servehttp.com"
response = requests.get(url)
logger.info(f"Sent a request to {url}. Received a response status code: {response.status_code}")

url = "https://swapi.info/api/films"
response = requests.get(url)
logger.info(f"Sent a request to {url}. Received a response status code: {response.status_code}")

FILE_PATH = "./data/films.json"
with open(FILE_PATH, "w") as films_response:
    films_response.write(json.dumps(response.json()))
logger.info(f"Saved the response to {FILE_PATH}")