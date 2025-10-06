# Changelog

All notable changes to the Package Measurement Conversion API will be documented in this file.

## [1.0.0] - 2025-09-30

### Added
- Initial release of Package Measurement Conversion API
- FastAPI-based REST API implementation
- `/convert-measurements` endpoint for converting measurement strings
- `/history` endpoint for retrieving conversion history
- MySQL database integration for persistent storage
- Character to value mapping (a-z = 1-26, underscore = 0)
- Special 'z' character handling (must combine with next character)
- Docker containerization with Dockerfile
- Docker Compose configuration for easy deployment
- Comprehensive logging system with console and file output
- Log rotation with 7-day retention
- Database health checks in docker-compose
- Volume mounting for logs directory
- Automatic database initialization on startup
- README.md with setup and usage instructions
- Error handling for invalid inputs and edge cases
- JSON response format with timestamps
- Environment variable configuration for database connection

### Features
- **Conversion Logic**: Implements measurement string to numeric value conversion
- **History Tracking**: All conversions are stored in MySQL database
- **Logging**: Rotating file logs with 7-day retention + console output
- **Containerization**: Fully containerized application with docker-compose
- **Production Ready**: Health checks, proper error handling, and logging

### Technical Details
- Python 3.11
- FastAPI 0.104.1
- MySQL 8.0
- Uvicorn ASGI server
- Modular architecture with separate converter and database manager classes

---

## [Unreleased]

### Planned
- Authentication and authorization
- Rate limiting per IP address
- Batch conversion endpoint
- Export history to CSV/JSON
- Prometheus metrics endpoint
- Enhanced error messages with suggestions
- Caching layer for frequently converted strings
- Web UI for easier testing
- API versioning (v2 endpoints)