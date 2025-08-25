from loginImplemenation import (
    get_api_logger, get_db_logger, get_app_logger,
    log_api_call, log_db_operation
)

# Example usage for API logging
def run_api_example():
    api_logger = get_api_logger("googlemaps")
    log_api_call(
        api_logger,
        method="GET",
        url="https://maps.googleapis.com/maps/api/directions/json",
        params={"origin": "home", "destination": "work"}
        headers={"User-Agent": "OrbitXO", "api-key": "SECRET"},
        response=type('Response', (), {"status_code": 200, "elapsed": "120ms"})(),
        error=None
    )

# Example usage for DB logging
def run_db_example():
    db_logger = get_db_logger("travel_times")
    log_db_operation(
        db_logger,
        operation="INSERT",
        table="travel_times",
        query="INSERT INTO travel_times (source, destination, duration) VALUES (?, ?, ?)",
        params=("home", "work", 26),
        result=[{"id": 1, "duration": 26}],
        error=None
    )

# Example usage for App logging
def run_app_example():
    app_logger = get_app_logger("notifier")
    app_logger.warning("Failed to send Slack notification, retrying...")
    app_logger.info("Slack notification sent successfully")

if __name__ == "__main__":
    run_api_example()
    run_db_example()
    run_app_example()
