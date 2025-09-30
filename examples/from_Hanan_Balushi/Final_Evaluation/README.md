# Package Measurement Conversion API

A REST API for converting measurement input strings into total values of measured inflows for each package.

## Features

- FastAPI-based REST API
- MySQL database for persistent history storage
- Comprehensive logging with 1-week rotation
- Docker containerization with docker-compose

## Measurement Conversion Rules

The API converts encoded measurement strings using the following rules:

- **Underscore (`_`)**: Represents 0
- **Characters `a` to `z`**: Represent values 1 to 26 respectively
  - `a` = 1, `b` = 2, ... `y` = 25, `z` = 26
- **Character `z` special rule**: Cannot stand alone; must be combined with the next character
  - `z` followed by any character = 26 + next character's value
  - Example: `za` = 26 + 1 = 27, `zb` = 26 + 2 = 28, `zz` = 26 + 26 = 52
- **Multi-character numbers**: For consecutive `z` characters, each `z` combines with the next character
  - Example: `zza` = (26 + 26) + 1 = 53
- **Number termination**: A number ends when a non-'z' character is encountered
- **Package format**: Each package consists of a count followed by measured values

### Examples

- `aa` → Package with count=1, value=1 → Result: `[1]`
- `bab` → Package with count=2, values=[1,2] → Result: `[3]` (sum: 1+2)
- `cabc` → Package with count=3, values=[1,2,3] → Result: `[6]` (sum: 1+2+3)
- `a_` → Package with count=1, value=0 → Result: `[0]`
- `aza` → Package with count=1, value=27 (z+a) → Result: `[27]`
- `zaa...` → Package with count=27 (z+a=26+1), followed by 27 'a' values → Result: `[27]`

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 1.29 or higher)

## Setup and Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Final_Evaluation
```

### 2. Project Structure

```
.
├── main_app.py                 # Main FastAPI application
├── measurement_converter.py    # Conversion logic
├── database_manager.py         # Database operations
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container image definition
├── docker-compose.yml          # Multi-container setup
├── CHANGELOG.md               # Version history and changes
├── version.txt                # Current version number
├── README.md                  # This file
└── logs/                      # Application logs (created automatically)
```

## Running the Application

### Using Docker Compose (Recommended)

1. **Start the application**:
```bash
docker-compose up -d
```

This command will:
- Build the API Docker image
- Start MySQL database container
- Start the API container
- Mount the logs directory to `./logs` on the host

2. **Check the status**:
```bash
docker-compose ps
```

3. **View logs**:
```bash
docker-compose logs -f api
```

4. **Stop the application**:
```bash
docker-compose down
```

5. **Stop and remove volumes** (caution: deletes database data):
```bash
docker-compose down -v
```


## API Endpoints

### 1. Convert Measurements

**Endpoint**: `GET /convert-measurements`

**Query Parameter**: `convert-measurements` (string) - The measurement input string

**Example Request**:
```bash
curl "http://localhost:8080/convert-measurements?convert-measurements=cabc"
```

**Example Response**:
```json
{
  "input": "cabc",
  "result": [6],
  "timestamp": "2025-09-29T10:30:45.123456"
}
```

### 2. Get Conversion History

**Endpoint**: `GET /history`

**Query Parameter**: `limit` (optional, default: 100) - Maximum number of records to retrieve

**Example Request**:
```bash
curl "http://localhost:8080/history?limit=10"
```

**Example Response**:
```json
{
  "count": 2,
  "history": [
    {
      "id": 2,
      "input_string": "cabc",
      "result": [6],
      "timestamp": "2025-09-29T10:30:45.123456"
    },
    {
      "id": 1,
      "input_string": "aaa",
      "result": [1],
      "timestamp": "2025-09-29T10:25:30.654321"
    }
  ]
}
```

### 4. Changelog Endpoint

**Endpoint**: `GET /changelog`

**Example Request**:
```bash
curl "http://localhost:8080/changelog"
```

**Example Response**:
```json
{
  "version": "1.0.0",
  "changelog": "# Changelog\n\nAll notable changes..."
}
```

## Logging

The application implements comprehensive logging:

- **Console output**: All log messages are printed to the console
- **File logging**: Logs are written to `logs/app.log`
- **Log rotation**: Automatically rotates logs with 7-day retention (1 week)
- **Log levels**: INFO level for normal operations, ERROR for failures

Access logs without entering the container:
```bash
tail -f logs/app.log
```

## Database

The application uses MySQL to persist conversion history:

- **Database**: `measurement_db`
- **User**: `measurement_user`
- **Table**: `conversion_history`
  - `id`: Auto-increment primary key
  - `input_string`: The input measurement string
  - `result`: JSON array of conversion results
  - `timestamp`: When the conversion was performed

Access the database:
```bash
docker exec -it measurement_mysql mysql -u measurement_user -p measurement_db
# Password: measurement_pass
```

## Troubleshooting

### Database Connection Issues

If the API cannot connect to MySQL:

1. Check if MySQL container is healthy:
```bash
docker-compose ps
```

2. Wait for MySQL to fully start (may take 20-30 seconds on first run)

3. Restart the API container:
```bash
docker-compose restart api
```

### Port Already in Use

If port 8080 is already in use:

1. Stop the conflicting service
```

### Viewing Container Logs

```bash
# API logs
docker-compose logs -f api

# MySQL logs
docker-compose logs -f mysql

# All logs
docker-compose logs -f
```

##