from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse
from datetime import datetime
import dotenv
import os

dotenv.load_dotenv()

# import only unique helpers from your workspace
from logging_im import fetch_route_with_retry, send_slack_message
from slack_alert_minimum_time import load_min_times, save_min_times

app = FastAPI(title="Unified Travel Time API")

# load persisted minimal times once
MIN_TIMES = load_min_times()


def _parse_duration_to_minutes(duration):
    """Accept '2700s', numeric seconds or minutes and return int minutes or None."""
    if duration is None:
        return None
    if isinstance(duration, str) and duration.endswith("s"):
        try:
            secs = int(duration[:-1])
        except ValueError:
            return None
    else:
        try:
            secs = int(duration)
        except Exception:
            return None
    return secs // 60


@app.get("/travel-time")
def travel_time(origin: str = Query(...), destination: str = Query(...)):
    # call the centralized fetch (with retry/logging) from logging_im
    result = fetch_route_with_retry(origin, destination)
    if not result or isinstance(result, dict) and "error" in result:
        detail = result.get("error") if isinstance(result, dict) else "Failed to get route"
        raise HTTPException(status_code=502, detail=detail)

    duration_raw = result.get("duration")
    distance_km = result.get("distance_km")

    duration_minutes = _parse_duration_to_minutes(duration_raw)
    if duration_minutes is None:
        raise HTTPException(status_code=500, detail=f"Unable to parse duration: {duration_raw}")

    key = f"{origin}->{destination}"
    prev_best = MIN_TIMES.get(key)

    new_record = False
    if prev_best is None or duration_minutes < prev_best:
        MIN_TIMES[key] = duration_minutes
        try:
            save_min_times(MIN_TIMES)
        except Exception as e:
            # do not fail the request because of persistence error; notify via Slack
            send_slack_message(f"⚠️ Could not save min_times: {e}")
        new_record = True

        saved_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_saved = (prev_best - duration_minutes) if prev_best is not None else 0
        alert_msg = (
            f"🚨 NEW RECORD TRAVEL TIME 🚨\n"
            f"Route: {origin} → {destination}\n"
            f"Current estimate: {duration_minutes} minutes\n"
            f"Previous best: {prev_best if prev_best is not None else 'N/A'} minutes\n"
            f"Time saved: {time_saved} minutes\n"
            f"Recorded at: {saved_at}"
        )
        send_slack_message(alert_msg)

    return {
        "origin": origin,
        "destination": destination,
        "duration_minutes": duration_minutes,
        "distance_km": distance_km,
        "new_record": new_record,
        "previous_best": prev_best,
    }


@app.get("/", response_class=HTMLResponse)
def root_ui():
    """Serve the UI.html file as the root page so visiting http://<host>:<port>/ shows the UI."""
    ui_path = os.path.join(os.path.dirname(__file__), "UI.html")
    try:
        with open(ui_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return HTMLResponse("<h1>UI file not found</h1><p>Place UI.html next to main.py</p>", status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)