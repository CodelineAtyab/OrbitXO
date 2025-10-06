# Changelog

All notable changes to this project will be documented in this file.

## [0.0.2] - 2025-09-29
- Added project changelog (`CHANGELOG.md`) and `version.txt` to record releases.

## [0.0.1] - 2025-09-29
Initial feature set:
- FastAPI HTTP endpoint GET `/convert-measurements?input=...` that processes strings into numeric lists.
- String processing rules: letter-to-value mapping (a=1..z=26), chained `z` rule for counts, item collection (single chars or z-chain items), non-letters produce standalone 0 entries.
- File logging via `log_config.py` (rotating file handler + console output).
- MySQL logging helper `logsql.py` that writes to a `requests_log` table and falls back to a JSONL file if the DB is unavailable.
- Dockerfile and `docker-compose.yml` to run the API and MySQL together. The compose file includes DB initialization `mysql-init/init.sql` and healthcheck.
