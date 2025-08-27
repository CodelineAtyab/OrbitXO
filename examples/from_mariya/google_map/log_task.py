# main_app.py
import logging
import logging.handlers
import os
import sys
import json
import time
import inspect
from datetime import datetime
from pathlib import Path
from typing import Optional

# =========================
# 1) Logging setup (daily rotation, keep 7 files)
# =========================
class LoggingConfig:
    """
    Separate loggers per component (api/database/notifier/main)
    Daily rotation at midnight, keep last 7 files, consistent format.
    """
    DEFAULT_LOG_DIR = "logs"

    def __init__(self, app_name: str = "travel_app",
                 log_dir: Optional[str] = None,
                 level: int = logging.INFO,
                 backup_count: int = 7,
                 console_output: bool = True):
        self.app_name = app_name
        self.log_dir = log_dir or self.DEFAULT_LOG_DIR
        self.level = level
        self.backup_count = backup_count
        self.console_output = console_output
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)
        self._configure_root()
        self._cache: dict[str, logging.Logger] = {}

    def _configure_root(self):
        root = logging.getLogger()
        for h in root.handlers[:]:
            root.removeHandler(h)
        root.setLevel(self.level)

    def _formatter(self):
        return logging.Formatter(
            "%(asctime)s %(levelname)s [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

    def get(self, name: str) -> logging.Logger:
        if name in self._cache:
            return self._cache[name]

        logger = logging.getLogger(name)
        logger.setLevel(self.level)
        logger.propagate = False

        file_path = Path(self.log_dir) / f"{self.app_name}_{name}.log"
        fh = logging.handlers.TimedRotatingFileHandler(
            str(file_path), when="midnight", backupCount=self.backup_count, encoding="utf-8"
        )
        fh.setFormatter(self._formatter())
        logger.addHandler(fh)

        if self.console_output:
            ch = logging.StreamHandler(sys.stdout)
            ch.setFormatter(self._formatter())
            logger.addHandler(ch)

        self._cache[name] = logger
        return logger

# =========================
# 2) Helper logging tools
# =========================
def log_function_call(logger: logging.Logger):
    """Decorator: DEBUG-log function calls, args/kwargs, and results."""
    def deco(func):
        def wrapper(*args, **kwargs):
            mod = inspect.getmodule(func).__name__
            logger.debug(f"Calling {mod}.{func.__name__} args={args} kwargs={kwargs}")
            try:
                res = func(*args, **kwargs)
                s = str(res)
                if len(s) > 1000:
                    s = s[:1000] + "... [truncated]"
                logger.debug(f"{mod}.{func.__name__} returned: {s}")
                return res
            except Exception as e:
                logger.error(f"{mod}.{func.__name__} raised {type(e).__name__}: {e}")
                raise
        return wrapper
    return deco

class LogExecutionTime:
    """Context manager: INFO-log success/elapsed or error/elapsed."""
    def __init__(self, logger: logging.Logger, name: str):
        self.logger = logger
        self.name = name
        self.start = None

    def __enter__(self):
        self.start = time.time()
        self.logger.info(f"Starting {self.name}")
        return self

    def __exit__(self, exc_type, exc, tb):
        elapsed = time.time() - self.start
        if exc_type:
            self.logger.error(f"{self.name} failed after {elapsed:.2f}s: {exc}")
        else:
            self.logger.info(f"Completed {self.name} in {elapsed:.2f}s")

# =========================
# 3) Components
# =========================
class ApiModule:
    """Mock API client to demonstrate logging."""
    def __init__(self, logs: LoggingConfig):
        self.log = logs.get("api")

    @log_function_call(logging.getLogger("api"))
    def request(self, url: str, params: dict):
        self.log.info(f"Starting API request to {url}")
        self.log.debug(f"Request parameters: {json.dumps(params)}")
        # simulate remote call (replace with requests if you want real HTTP)
        time.sleep(0.6)
        resp = {"status": 200, "reason": "OK", "data": {"result": "success"}}
        self.log.info(f"Received response: {resp['status']} {resp['reason']}")
        return resp

class DatabaseModule:
    """
    Tiny JSON 'database' stored at data/travel_state.json
    Schema example:
    {
      "travel_time": [
        {"source": "...", "destination": "...", "duration_minutes": 26, "timestamp": "..."}
      ]
    }
    """
    def __init__(self, logs: LoggingConfig, file_path: str = "data/travel_state.json"):
        self.log = logs.get("database")
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self._data = self._load()

    def _load(self) -> dict:
        if self.file_path.exists():
            try:
                self.log.info("Loading JSON DB from %s", self.file_path)
                return json.loads(self.file_path.read_text(encoding="utf-8"))
            except Exception as e:
                self.log.warning("Failed to read JSON DB, starting fresh: %s", e)
        return {}

    def _save(self):
        try:
            self.file_path.write_text(json.dumps(self._data, ensure_ascii=False, indent=2), encoding="utf-8")
            self.log.info("Saved JSON DB to %s", self.file_path)
        except Exception as e:
            self.log.error("Failed to save JSON DB: %s", e)

    def connect(self):
        # not a real DB connection; we just log the file being used
        self.log.info("Using JSON DB at %s", self.file_path)

    def store(self, table: str, data: dict):
        """Append a record to a list under the given table name."""
        self.log.info("Storing new %s record", table)
        self.log.debug("Record data: %s", json.dumps(data, ensure_ascii=False))
        self._data.setdefault(table, [])
        self._data[table].append(data)
        self._save()

    def get_all(self, table: str):
        return self._data.get(table, [])

class NotifierModule:
    """
    Simple Slack notifier (optional).
    If SLACK_WEBHOOK_URL is not set, it just logs.
    """
    def __init__(self, logs: LoggingConfig):
        self.log = logs.get("notifier")
        self.webhook = os.getenv("SLACK_WEBHOOK_URL")

    def send(self, channel: str, message: str) -> bool:
        self.log.info(f"Sending {channel} notification")
        # simulate either success or a transient failure with retry
        time.sleep(0.2)
        # If you want real Slack, uncomment the requests code below and ensure you installed 'requests'
        if not self.webhook:
            self.log.info("No SLACK_WEBHOOK_URL; logged only: %s", message)
            return True

        try:
            import requests  # local import so the file runs without it if you don't use Slack
            payload = {"text": message}
            r = requests.post(self.webhook, json=payload, timeout=10)
            if r.status_code == 200:
                self.log.info("Slack notification sent successfully")
                return True
            self.log.warning("Slack send failed (%s %s), retrying...", r.status_code, r.text)
            r2 = requests.post(self.webhook, json=payload, timeout=10)
            if r2.status_code == 200:
                self.log.info("Slack notification sent successfully on retry")
                return True
            self.log.error("Slack failed after retry: %s %s", r2.status_code, r2.text)
            return False
        except Exception as e:
            self.log.error("Slack error: %s", e)
            return False

# =========================
# 4) Demo flow
# =========================
def run_demo():
    logs = LoggingConfig(
        app_name="travel_app",
        level=logging.DEBUG,   # set to INFO in prod
        backup_count=7,
        console_output=True
    )

    main = logs.get("main")
    main.info("Application starting")

    try:
        api = ApiModule(logs)
        db = DatabaseModule(logs)
        notifier = NotifierModule(logs)

        with LogExecutionTime(main, "complete travel time request workflow"):
            # 1) API call (mocked)
            resp = api.request(
                url="https://maps.googleapis.com/maps/api/directions/json",
                params={"source": "home", "destination": "work"}
            )

            # 2) DB store
            db.connect()
            db.store("travel_time", {
                "source": "home",
                "destination": "work",
                "duration_minutes": 26,
                "timestamp": datetime.now().isoformat()
            })

            # (optional) read them back
            total = len(db.get_all("travel_time"))
            main.info("Total travel_time records: %s", total)

            # 3) Notify
            notifier.send("slack", "New travel time record created")

        main.info("Application completed successfully")
    except Exception as e:
        main.critical(f"Application failed with error: {e}", exc_info=True)

if __name__ == "__main__":
    run_demo()