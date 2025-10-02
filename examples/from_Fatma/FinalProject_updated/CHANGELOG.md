# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.3] - 2025-10-01
### Added
- Added `logsql.py` module with SQLLogger class for enhanced database operations
- Added `log_config.py` for application-wide logging configuration
- Added support for rotating log files with size limits
- Added console and file logging with formatted output
- Added support for pagination in log retrieval
- Added log cleanup functionality for maintenance

## [0.0.2] - 2025-10-01
### Added
- Added CHANGELOG.md for tracking project changes
- Added VERSION file to track current project version

## [0.0.1] - 2025-10-01
### Added
- Initial release of the Measurement Converter API
- FastAPI application with measurement conversion endpoint
- MySQL database integration for storing conversion history
- Docker and Docker Compose configuration
- Two API endpoints:
  - `/convert-measurements` for string conversion
  - `/history` for viewing conversion history
- README.md with usage instructions
- Database initialization script (init.sql)