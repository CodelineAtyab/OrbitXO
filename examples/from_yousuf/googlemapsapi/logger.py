import importlib as _importlib
logging = _importlib.import_module("logging")
from logging import Formatter, StreamHandler, FileHandler
import os

LEVELS = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "WARN": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET,
}

_default_formatter = Formatter(
    "%(asctime)s [%(levelname)s] %(name)s - %(message)s", "%Y-%m-%d %H:%M:%S"
)

def configure_logging(level="INFO", logfile=None, fmt=None):
    lvl = LEVELS.get(str(level).upper(), logging.INFO) if isinstance(level, str) else level
    root = logging.getLogger()
    root.setLevel(lvl)
    for h in list(root.handlers):
        root.removeHandler(h)
    formatter = fmt or _default_formatter
    sh = StreamHandler()
    sh.setLevel(lvl)
    sh.setFormatter(formatter)
    root.addHandler(sh)
    if logfile is None:
        base_dir = os.path.dirname(__file__)
        logs_dir = os.path.join(base_dir, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        logfile = os.path.join(logs_dir, "googlemapsapi.log")
    if logfile:
        fh = FileHandler(logfile)
        fh.setLevel(lvl)
        fh.setFormatter(formatter)
        root.addHandler(fh)

def get_logger(name=None):
    return logging.getLogger(name)
