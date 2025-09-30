# Package Measurement Conversion API

## Overview
An API that converts encoded package measurement strings into numerical lists, with persistent history in SQLite.

## Features
- Convert measurement strings to numeric package totals.
- Persist conversion history in SQLite (`db.sqlite3`).
- Dockerized for easy deployment.
- Logging to `logs/` directory.


## Prerequisites
- Docker & Docker Compose installed.
- Linux/macOS/Windows host.


## Run with Docker Compose
- ```bash
- Build/run the image/container --> docker-compose up --build
- Verify the container is running --> docker ps
- API available at --> http://localhost:8081

## API Endpoints
- Convert Measurements:
GET /convert-measurements?input=<string>

--- Example Request:
GET /convert-measurements?input=abbcc

--- Response:
[2, 6]

--- Get History - Returns all previous conversions stored in the database.
GET /history

--- Example Response:
[
  {"id": 1, "input": "abbcc", "output": "2,6"},
  {"id": 2, "input": "dz_a_aazzaaa", "output": "28,53,1"}
]

## Logs
Logs are written to logs/app.log - Mounted to host via Docker volume.


