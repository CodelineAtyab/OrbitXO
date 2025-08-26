import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

LOG_DIR = "logs"
LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
MAX_LOG_SIZE = 5 * 1024 * 1024  
BACKUP_COUNT = 7 k

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def get_logger(name, log_file=None, level=logging.INFO):

    if log_file is None:
        log_file = f"{name}.log"

    log_path = os.path.join(LOG_DIR, log_file)
    

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:

        file_handler = RotatingFileHandler(
            log_path, 
            maxBytes=MAX_LOG_SIZE,
            backupCount=BACKUP_COUNT
        )
        file_handler.setLevel(level)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

root_logger = get_logger("app", "application.log")

api_logger = get_logger("api", "api.log")
database_logger = get_logger("database", "database.log")
notifier_logger = get_logger("notifier", "notifier.log")

def set_debug_mode():
    root_logger.setLevel(logging.DEBUG)
    api_logger.setLevel(logging.DEBUG)
    database_logger.setLevel(logging.DEBUG)
    notifier_logger.setLevel(logging.DEBUG)

    def __init__(self, logger, context):
        self.logger = logger
        self.original_format = LOG_FORMAT
        self.context = context
        
    def __enter__(self):
        for handler in self.logger.handlers:
            formatter = handler.formatter
            if formatter:
                context_format = LOG_FORMAT.replace(
                    "%(message)s", 
                    f"[{self.context}] %(message)s"
                )
                handler.setFormatter(
                    logging.Formatter(context_format, DATE_FORMAT)
                )
        return self.logger
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        for handler in self.logger.handlers:
            handler.setFormatter(
                logging.Formatter(self.original_format, DATE_FORMAT)
            )
