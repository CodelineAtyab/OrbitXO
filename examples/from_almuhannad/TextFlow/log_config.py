import logging
from logging.handlers import TimedRotatingFileHandler
import os



def setup_logger(name='api_logger', level=logging.INFO):
    LOGS_dir = "logs"
    if not os.path.exists(LOGS_dir):
        os.makedirs(LOGS_dir)

    LOG_FILE = os.path.join(LOGS_dir, "api.log")

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = TimedRotatingFileHandler(
            LOG_FILE, 
            when="W0",
            interval=1, 
            backupCount=1
        )
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

logger = setup_logger()