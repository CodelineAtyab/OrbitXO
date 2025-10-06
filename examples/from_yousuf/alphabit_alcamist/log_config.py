import os
import logging
from logging.handlers import TimedRotatingFileHandler

# Environment-driven defaults
LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_FILENAME = os.getenv("LOG_FILENAME", "api.log")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "2"))  # keep a couple of rotations

os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, LOG_FILENAME)

# Create and configure logger
_service_logger = logging.getLogger("service_logger")
_service_logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

# File handler: rotate every 7 days (midnight rotation with interval=7)
file_handler = TimedRotatingFileHandler(
    LOG_PATH,
    when="midnight",
    interval=7,
    backupCount=BACKUP_COUNT,
    utc=True,
)
file_formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s:%(module)s] %(message)s")
file_handler.setFormatter(file_formatter)

# Console handler for immediate output during development/runtime
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter("%(levelname)s: %(message)s")
console_handler.setFormatter(console_formatter)

# Avoid attaching duplicate handlers on repeated imports
if not _service_logger.handlers:
    _service_logger.addHandler(file_handler)
    _service_logger.addHandler(console_handler)

def get_logger() -> logging.Logger:
    """Return the configured logger instance."""
    return _service_logger

# Module-level convenience variable expected by other modules
api_logger = get_logger()