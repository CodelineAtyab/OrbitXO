# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2025-09-29

### Added
- Implemented a changelog (`changelog.md`) to track project changes.
- Introduced a `version.txt` file for version management.

## [0.0.1] - 2025-09-29

### Added
- **Initial Setup**:
    - Created a FastAPI microservice in `main.py` featuring a `/convert-measurements` endpoint.
    - Developed a custom algorithm for converting string-based measurements to numerical values.
    - Implemented a comprehensive logging system using `logsql.py` and `log_config.py` to record requests in both a log file and a MySQL database.
    - Added Docker containerization support via `Dockerfile` and `docker-compose.yml` for the application and its MySQL database.
    - Included an initialization script (`mysql-init/init.sql`) for the MySQL database.
