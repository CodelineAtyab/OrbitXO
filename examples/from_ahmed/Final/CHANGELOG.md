# Changelog

All notable changes for this project. This file was generated from the accompanying README in the same folder.

## [0.0.2] - 2025-09-29
- Added this `CHANGELOG.md` file and a `version.txt` file.
- Bumped package version to `0.0.2`.

## [0.0.1] - 2025-09-29
Initial release — FastAPI Measurement Converter

### Features
- FastAPI application that converts input strings into numeric segment sums using custom rules (a=1, b=2, ...; `z` absorbs the next character).
- API implemented in `Finaleval.py` with both GET and POST endpoints: `/measurement-convert?input_str=...` and POST JSON `{ "input_str": "..." }`.
- Interaction logging to both MySQL and a file:
  - MySQL logger in `db_logger.py` (creates `logsdb.history` table if missing).
  - File logger in `file_logger.py` (writes JSON-lines to `app_interactions.log`).
- Included supporting files: `schema.sqlschemmac`, `Dockerfile`, `docker-compose.yml`, and `requirements.txt`.
- Docker Compose support to run a MySQL container and the FastAPI app (app exposed on port 8080).
- Local development instructions and examples included (how to run with Docker, install deps, and run with `uvicorn`).
- Logs & database details: file log path configurable by `LOG_FILE`; DB is `logsdb` with `history(id, input_str, result, timestamp)`.
- Environment variables supported: `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `LOG_FILE`.
- Troubleshooting notes and suggested next improvements (DB readiness retry, Alembic, unit tests).

### Notes
- See `README.md` in this folder for full usage, examples, and troubleshooting steps.
