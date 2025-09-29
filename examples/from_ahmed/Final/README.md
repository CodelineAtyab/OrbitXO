# FastAPI Measurement Converter

Small FastAPI service that converts input strings into numeric segment sums using custom rules (a=1, b=2, ...; `z` absorbs the next character). Each API interaction is logged to both a MySQL database and a file.

## Contents
- `Finaleval.py` - FastAPI application and conversion logic
- `db_logger.py` - MySQL logger (creates `logsdb.history` table if missing)
- `file_logger.py` - Appends JSON-lines to `app_interactions.log`
- `schema.sqlschemmac` - SQL to create database & `history` table
- `Dockerfile` - Container image for the FastAPI app
- `docker-compose.yml` - Starts MySQL and the FastAPI app
- `requirements.txt` - Python dependencies

## Quick summary of behavior
- The first character of a segment is the counter (a=1, b=2, ..., z special). The following characters (count many) are summed using letter values. `z` always absorbs the next character as part of its value (recursively if chained).

Example: input `abcee` -> `a` (count=1) takes `b` (2) -> first result 2. `c` (count=3) takes `e`,`e` (5+5) -> second result 10. Response: `{ "result": [2, 10] }`.

---

## Prerequisites
- Docker & Docker Compose
- (Optional) Python 3.11+ for local development

## Run with Docker Compose (recommended)
This will start a MySQL 8 container and the FastAPI app (exposed on port 8080).

From the project root run:

```powershell
docker compose up --build -d
```

Watch logs:

```powershell
docker compose logs -f app
docker compose logs -f db
```

Stop and remove containers:

```powershell
docker compose down
```

## Run locally (without Docker)
1. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

2. Ensure a MySQL server is available and reachable. You can run just the DB via Docker Compose:

```powershell
docker compose up -d db
```

3. Export environment variables (PowerShell example):

```powershell
$env:DB_HOST = "127.0.0.1"; $env:DB_PORT = "3306"; $env:DB_USER = "user"; $env:DB_PASSWORD = "password"; $env:DB_NAME = "logsdb"
python Finaleval.py
```

Or run with uvicorn (if installed):

```powershell
uvicorn Finaleval:app --host 0.0.0.0 --port 8080 --reload
```

## API Endpoints
- GET /measurement-convert?input_str=YOUR_STRING
- POST /measurement-convert  (JSON body: `{ "input_str": "..." }`)

Examples (curl):

```powershell
curl "http://localhost:8080/measurement-convert?input_str=abcee"

curl -X POST http://localhost:8080/measurement-convert -H "Content-Type: application/json" -d '{"input_str":"abcee"}'
```

## Logs & Database
- File log is written to `app_interactions.log` (JSON-lines). The path can be configured with the `LOG_FILE` env variable.
- MySQL database `logsdb`, table `history` (columns: `id`, `input_str`, `result` JSON, `timestamp`). The `schema.sqlschemmac` file contains the SQL to create the DB/table if needed.

Apply schema manually (optional):

Use a MySQL client to execute `schema.sqlschemmac` if you need to apply the schema by hand.

## Environment variables
- `DB_HOST` (default: `db` when run in Docker compose)
- `DB_PORT` (default: `3306`)
- `DB_USER` (default: `user`)
- `DB_PASSWORD` (default: `password`)
- `DB_NAME` (default: `logsdb`)
- `LOG_FILE` (default: `app_interactions.log`)

## Troubleshooting
- Container won't start because DB is not ready: MySQL may take a moment to initialize. Check `docker compose logs db` and retry.
- `uvicorn` or DB connector missing errors: install dependencies from `requirements.txt`.
- File permission errors writing `app_interactions.log`: ensure container/user has write permissions.

## Next improvements (optional)
- Add a small start-up wait/retry for DB readiness.
- Use Alembic for DB migrations rather than `CREATE TABLE IF NOT EXISTS`.
- Add unit tests for `measurement_converter` and CI.


