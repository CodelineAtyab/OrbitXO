import os
import sys
import logging
from logging.handlers import RotatingFileHandler


# If directory doesn't exist then create
os.makedirs('./logs', exist_ok=True)

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

logger = logging.getLogger(__name__)