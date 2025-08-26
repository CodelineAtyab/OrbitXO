
import logging
from contextvars import ContextVar

current_request_id = ContextVar("request_id", default="-")
current_user = ContextVar("user", default="-")

class ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # Inject contextual fields into the record, always present
        record.request_id = current_request_id.get()
        record.user = current_user.get()
        return True

class request_context:
    """Context manager to set request_id and user for logs."""
    def __init__(self, request_id: str, user: str = "-"):
        self._rid = request_id or "-"
        self._user = user or "-"
        self._t1 = None
        self._t2 = None

    def __enter__(self):
        self._t1 = current_request_id.set(self._rid)
        self._t2 = current_user.set(self._user)
        return self

    def __exit__(self, exc_type, exc, tb):
        # Reset to previous values
        current_request_id.reset(self._t1)
        current_user.reset(self._t2)
        return False
