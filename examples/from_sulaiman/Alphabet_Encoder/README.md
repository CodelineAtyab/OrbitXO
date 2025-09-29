# Alphabet Encoder API

A FastAPI-based service that encodes alphabetical input strings and stores logs in both MySQL database and log files.

## Project Overview

This project provides a RESTful API service that processes string inputs using an alphabet-based encoding algorithm. The service logs all requests and responses to a MySQL database and log files for auditing and monitoring purposes.

## Features

- **Alphabet Encoding Algorithm**: Converts input strings into numerical values based on character positions
- **RESTful API**: Built with FastAPI for high-performance API endpoints
- **Containerized Architecture**: Uses Docker and Docker Compose for easy deployment
- **Persistent Storage**: MySQL database for structured data storage
- **Comprehensive Logging**: Dual-logging system (database + files) with rotation
- **Health Checks**: Database connectivity checks with retry mechanism
- **Resilient Infrastructure**: Auto-reconnect capabilities and proper service dependencies

## Architecture

The project consists of two main services:

1. **API Service**: FastAPI application that processes requests and performs encoding
2. **Database Service**: MySQL database to store request logs

Both services run as Docker containers managed by Docker Compose, with persistent volumes for data and logs.

## API Endpoints

### Encode Input

```
GET /?input={input_string}
```

**Parameters**:
- `input_string`: The string to be encoded

**Response**:
```json
{
  "output": [int_array]
}
```

## Requirements

- Docker
- Docker Compose

## Setup and Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd Alphabet_Encoder
```

2. Build and start the services:

```bash
docker-compose up -d
```

3. The API will be available at http://localhost:8010

## Usage Examples

**Request**:
```bash
curl "http://localhost:8010/?input=abc123"
```

**Response**:
```json
{
  "output": [2, 0]
}
```

## Project Structure

```
├── alphabet_encoder.py  # Main API application
├── sql_logs.py          # Database and logging functionality
├── Dockerfile           # API container definition
├── docker-compose.yml   # Service orchestration
├── requirements.txt     # Python dependencies
├── .dockerignore        # Files excluded from Docker build
└── logs/                # Directory for log files
    ├── app.log          # Application logs
    └── api_requests.log # API request/response logs
```

## Logs

Logs are stored in two places:

1. **MySQL Database**: Table `logs` contains:
   - Timestamp
   - Input string
   - Output result

2. **Log Files**:
   - `logs/app.log`: Application-level logs
   - `logs/api_requests.log`: API request/response logs in JSON format

## Database Schema

```sql
CREATE TABLE logs (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  input TEXT,
  output TEXT
);
```

## Docker Setup

The project uses Docker Compose to manage:

- API service (FastAPI)
- MySQL database
- Persistent volumes for data and logs

## Environment Variables

The following environment variables can be configured in the docker-compose.yml:

- `MYSQL_HOST`: MySQL server hostname
- `MYSQL_USER`: MySQL username
- `MYSQL_PASSWORD`: MySQL password
- `MYSQL_DATABASE`: MySQL database name
- `LOG_DIR`: Directory for log files

## Development

To extend or modify this project:

1. Make changes to the code
2. Rebuild the Docker containers:
```bash
docker-compose up --build -d
```

## Maintenance

### Viewing Logs

**Application logs**:
```bash
docker-compose exec api cat /app/logs/app.log
```

**API request logs**:
```bash
docker-compose exec api cat /app/logs/api_requests.log
```

**Database logs**:
```bash
docker-compose logs db
```

### Database Management

**View logged data**:
```bash
docker-compose exec db mysql -u root -ppassword -e "USE alphabet_logs; SELECT * FROM logs;"
```

## Troubleshooting

### Common Issues

**API can't connect to database**:
1. Check if the database container is running: `docker-compose ps`
2. Verify the MySQL service is healthy: `docker-compose logs db`
3. Ensure environment variables are correctly set in docker-compose.yml

**Log files not being created**:
1. Check if the logs volume is correctly mounted
2. Verify permissions in the logs directory

## License

[Add your license information here]