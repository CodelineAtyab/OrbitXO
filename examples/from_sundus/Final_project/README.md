# Package Measurement Conversion API

A FastAPI application that converts input strings into numerical measurements and stores the history in a database. Fully containerized with Docker and compatible with MySQL 8 or SQLite.

## Features

- `/convert-measurements` endpoint:
  - Input: string
  - Output: list of integers representing converted measurements
  - Stores each request and result in the database.
- `/history` endpoint:
  - Returns the latest conversion records.
- Supports SQLite (default) or MySQL 8 via environment variable `DATABASE_URL`.
- Daily rotating logs.
- Dockerized for easy deployment.
- Handles MySQL 8 authentication with `cryptography`.

## Requirements

- Docker & Docker Compose
- Python 3.11 (if running outside Docker)

## Installation & Running

### Using Docker Compose

1. Clone the repository:
```bash
git clone <repo_url>
cd <repo_folder>
