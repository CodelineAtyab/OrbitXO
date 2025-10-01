# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - Initial Release
### Added
- `main_app.py`: FastAPI application for package measurement conversion.
  - `/convert-measurements` endpoint to convert input strings to numerical results.
  - `/history` endpoint to retrieve the last 50 conversion records.
  - SQLite or MySQL backend support via SQLAlchemy.
  - Logging system with daily rotating log files.
- `convert_measurements` function for string-to-number conversion logic.
- Database retry mechanism to handle MySQL startup delays.
- `History` table model to store conversion history.

- `wait-for-db.py`: Script to wait for MySQL readiness before starting FastAPI (optional, supports Docker Compose).
- `requirements.txt`: Required Python packages (`fastapi`, `uvicorn`, `sqlalchemy`, `pymysql`, `cryptography`).
- `Dockerfile`: Containerized Python 3.11 slim image setup.
  - Installs system dependencies for MySQL and `cryptography`.
  - Converts Windows line endings to Unix.
  - Runs FastAPI via Uvicorn.
- `docker-compose.yml`: Multi-container setup with:
  - MySQL 8 database container with persistent volume.
  - FastAPI API container depending on MySQL health.
  - Environment variables for DB credentials and logging.
- Added support for MySQL 8 `caching_sha2_password` authentication with `cryptography`.

### Fixed
- Handled MySQL connection errors with retry loops.
- Resolved `cryptography` requirement for MySQL 8 authentication.

### Notes
- MySQL warning regarding `/var/run/mysqld` directory permissions is normal for development.
- API accessible at `http://localhost:8000` (Uvicorn).
- Swagger documentation available at `http://localhost:8000/docs`.
