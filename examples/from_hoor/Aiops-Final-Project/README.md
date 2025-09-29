# Package Measurement Conversion API

## Setup

1. Clone the repo and navigate into it.
2. Run with docker-compose:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8080`.

## Endpoints

- `/convert-measurements?input=<string>` → Returns decoded list
- `/history` → Returns stored history

## Example

```bash
curl "http://localhost:8080/convert-measurements?input=abbcc"
# [2, 6]
```

## Requirements

- Docker
- Docker Compose
