# CHANGELOG

## version [0.0.4] - 30-09-2025
### Fixed 
- Modify README.md file.



## version [0.0.3] - 29-09-2025
### Fixed 
- Modify the port in docker-compose file.



## version [0.0.2] - 29-09-2025
### Added 
- Dockerfile and docker-compose for containerized deployment.
- SQLite3 database integration for storing request history.
- handling rule for `_` string.



## version [0.0.1] - 28-09-2025
### Added
- Initial release of Package Measurement Conversion API.
- Core algorithm for parsing measurement strings (`converter.py`).
- FastAPI server with `/convert-measurements` endpoint.
- Logging system with file output to `logs/app.log`.
- Unit tests for algorithm in `tests/test_converter.py`.

