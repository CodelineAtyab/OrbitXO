# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2025-09-29

### Added
- A `CHANGELOG.md` file was added to the project.
- A versioning system was introduced.

## [0.0.1] - 2025-09-29

### Added
- **Initial Project Creation**:
    - FastAPI microservice (`main.py`) with a `/convert-measurements` endpoint.
    - Custom string-to-number conversion algorithm.
    - Dual logging system (`logsql.py`, `log_config.py`) to log requests to both a file and a MySQL database.
    - Docker support (`Dockerfile`, `docker-compose.yml`) for containerizing the application and a MySQL database.
    - MySQL database initialization script (`mysql-init/init.sql`).