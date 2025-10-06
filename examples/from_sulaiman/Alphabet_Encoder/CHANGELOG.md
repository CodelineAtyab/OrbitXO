# Changelog

All notable changes to the Alphabet Encoder project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2025-09-29

### Added
- CHANGELOG.md file to track all project changes
- VERSION.txt file to indicate current project version
- Versioning system following Semantic Versioning principles

### Changed
- Updated documentation to reflect the versioning system
- Enhanced README.md with changelog information

## [0.0.1] - 2025-09-15

### Added
- Initial implementation of the Alphabet Encoder API
- FastAPI framework integration
- Alphabet encoding algorithm that converts input strings into numerical values
- Docker and Docker Compose configuration for containerized deployment
- MySQL database integration for persistent storage
- Dual-logging system (database + files)
  - Database logging with SQLAlchemy
  - File logging with rotation support
- Environment variable configuration
- README.md with comprehensive documentation
- Health check mechanisms for database connections
- Auto-reconnect capabilities and service dependencies

### Technical Details
- Created alphabet_encoder.py with the main FastAPI application
  - GET endpoint that processes string inputs and returns encoded values
  - Algorithm that assigns numerical values based on character positions
- Implemented sql_logs.py for database and logging functionality
  - SQLAlchemy models for database interaction
  - Logging setup with RotatingFileHandler
  - Database retry mechanism for resilience
- Containerized application using Docker
  - Multi-container setup with Docker Compose
  - Persistent volumes for logs and database
- Configured health checks for database connectivity
- Implemented API request/response logging