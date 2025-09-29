# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2025-09-29

### Added
- `CHANGELOG.md` to document project versions and changes.
- `VERSION` file to track the current version of the application.

## [0.0.1] - 2025-09-29

### Added
- Initial project setup with a containerized FastAPI application.
- Middleware to automatically intercept and log all HTTP requests and responses.
- Docker Compose configuration to orchestrate the application (`app`) and database (`db`) services.
- MySQL database service for persistent storage of API logs.
- An initialization script (`mysql-init/init.sql`) to automatically create the `requests_log` table.
- A `DatabaseLogger` class to handle all database connections and logging logic.
- A comprehensive `README.md` file with a project summary, architectural overview, and deployment instructions.
