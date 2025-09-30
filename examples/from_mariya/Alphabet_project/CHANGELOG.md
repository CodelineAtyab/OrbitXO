# 📜 Changelog

All notable changes to this project will be documented in this file.

## [1.0.1] - 2025-09-28
### Added
- Added `version.txt` to track the project version.
- Added `CHANGELOG.md` to document project changes.
- Added `.gitignore` for cleaner version control (ignoring cache, logs, venv).
- Performed additional testing with alternative input strings to verify decoding logic.

## [1.0.0] - 2025-09-28
### Added
- Initial release of the Alphabet Alchemist API.
- Added `/convert-measurements` endpoint to decode letter-based measurement strings.
- Added `/history` endpoint to fetch saved results from MySQL.
- Implemented MySQL integration using Docker Compose with persistent volumes.
- Logging system writes to `logs/app.log`.
- Added `test_decoder.py` with full Pytest coverage for all given examples.
- Created `init.sql` for automatic database initialization on first startup.
- Added `README.md` with setup and usage instructions.
