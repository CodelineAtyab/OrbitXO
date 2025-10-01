# Measurement Converter API

This application provides a REST API for converting measurement strings and storing the conversion history in MySQL.

## Prerequisites

- Docker
- Docker Compose

## Running the Application

1. Navigate to the project directory
2. Run:
```
docker compose up --build
```

The application will be available at:
- API endpoint: http://localhost:8080
- Test the converter: http://localhost:8080/convert-measurements?input=b_ab
- View history: http://localhost:8080/history

## API Endpoints

- GET `/convert-measurements?input=<string>`: Convert a measurement string
- GET `/history`: View conversion history

## Example Usage

```
# Convert a measurement
curl "http://localhost:8080/convert-measurements?input=b_ab"

# View history
curl "http://localhost:8080/history"
```

## Stopping the Application

To stop the application:
```
docker compose down
```

To stop and remove all data (including the MySQL database):
```
docker compose down -v
```