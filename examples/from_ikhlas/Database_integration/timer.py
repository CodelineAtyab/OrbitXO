from apscheduler.schedulers.background import BackgroundScheduler
from app import record_travel_time
import time

scheduler=BackgroundScheduler()

source="Muscat Private Hospital, Muscat, Oman"
dest="Codeline, Muscat, Oman"

# Run every 15 minutes
scheduler.add_job(record_travel_time, "interval", minutes=15, args=[source, dest])
scheduler.start()

print("[INFO] Timer started. Running for 2 hours (8 runs)...")

try:
    time.sleep(60 * 120)  # run for 2 hours
except (KeyboardInterrupt, SystemExit):
    pass
finally:
    scheduler.shutdown()
    print("[INFO] Scheduler stopped after 2 hour.")
