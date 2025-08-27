import logging
from logging.handlers import TimedRotatingFileHandler
import os

LOG_DIR = "log"
os.makedirs(LOG_DIR,exist_ok=True)

def log_setup(componant):

    logger = logging.getLogger(componant)
    logger.setLevel(logging.DEBUG)
    log_file = os.path.join(LOG_DIR, f"{componant}.log")
    handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=7)
    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(filename)s] %(message)s')
    handler.setFormatter(formatter)

    return logger

