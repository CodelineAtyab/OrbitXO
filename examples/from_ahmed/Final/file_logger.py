import os
import json
import datetime

LOG_FILE = os.getenv('LOG_FILE', 'app_interactions.log')

def _ensure_log_dir(path: str):
    directory = os.path.dirname(os.path.abspath(path))
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def save_log(input_str: str, result: list):
    """Append a JSON line to the log file with timestamp, input and result."""
    _ensure_log_dir(LOG_FILE)
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'input_str': input_str,
        'result': result,
    }
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def init_file_logger():
    # Create file if missing
    _ensure_log_dir(LOG_FILE)
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'a', encoding='utf-8').close()
