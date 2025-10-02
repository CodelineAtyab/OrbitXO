import logging
import os
import sys

# إنشاء مجلد logs لو مش موجود
LOG_DIR = os.environ.get("LOG_DIR", "./logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR, "app.log")

# إعداد اللوج
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),   # يخزن في ملف
        logging.StreamHandler(sys.stdout)     # يطبع في التيرمنال
    ]
)

logger = logging.getLogger("aiops_logger")
