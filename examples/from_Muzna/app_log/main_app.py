import requests
import logging
import sys
from logging.handlers import RotatingFileHandler

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(
    format=FORMAT,
    level=logging.DEBUG,
    handlers=[
        RotatingFileHandler(
            "./app.log",
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=7,
            encoding="utf-8",
            mode="a"
        ),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("app")

# API 
url = "https://aiops.servehttp.com"
response = requests.get(url)
logger.info(f"Request to {url} returned status code {response.status_code}")
