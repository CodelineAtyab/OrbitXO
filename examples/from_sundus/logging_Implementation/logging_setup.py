
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from utils import ContextFilter

DEFAULT_LOG_DIR = os.getenv("LOG_DIR", "logs")
DEFAULT_LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
SPLIT_LOGS = os.getenv("SPLIT_LOGS", "false").lower() in {"1","true","yes","y"}

LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] [req:%(request_id)s user:%(user)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def _ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def _make_file_handler(path: Path) -> TimedRotatingFileHandler:
    handler = TimedRotatingFileHandler(
        filename=str(path), when="midnight", interval=1, backupCount=7, encoding="utf-8"
    )
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    handler.addFilter(ContextFilter())
    return handler

def _make_console_handler() -> logging.Handler:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    handler.addFilter(ContextFilter())
    return handler

def setup_logging() -> None:
    """Configure root + module loggers with rotation and context.

    Env vars:
      LOG_DIR    -> directory for log files (default: logs)
      LOG_LEVEL  -> DEBUG/INFO/WARNING/ERROR (default: INFO)
      SPLIT_LOGS -> true to write api/database/notifier to separate files
    """
    log_dir = Path(DEFAULT_LOG_DIR)
    _ensure_dir(log_dir)

    root_logger = logging.getLogger()
    # Prevent duplicate handlers if called twice
    if getattr(root_logger, "_configured", False):
        return
    root_logger._configured = True

    # set root level
    root_logger.setLevel(getattr(logging, DEFAULT_LOG_LEVEL, logging.INFO))

    # Console handler
    console = _make_console_handler()
    root_logger.addHandler(console)

    if SPLIT_LOGS:
        # Separate files for each component
        api_h = _make_file_handler(log_dir / "api.log")
        db_h = _make_file_handler(log_dir / "database.log")
        ntf_h = _make_file_handler(log_dir / "notifier.log")
        app_h = _make_file_handler(log_dir / "app.log")

        logging.getLogger("api").addHandler(api_h)
        logging.getLogger("database").addHandler(db_h)
        logging.getLogger("notifier").addHandler(ntf_h)
        # App-level (root or main) logs go to app.log via root handler
        root_logger.addHandler(app_h)
    else:
        # Single file for everything
        file_h = _make_file_handler(log_dir / "app.log")
        root_logger.addHandler(file_h)

    # Make sure child loggers propagate to root
    for name in ("api", "database", "notifier"):
        logging.getLogger(name).setLevel(logging.DEBUG)  # capture DEBUG when root allows it
        logging.getLogger(name).propagate = True
