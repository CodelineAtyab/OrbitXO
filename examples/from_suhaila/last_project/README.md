# Letter Value Conversion API

A FastAPI application that converts text into numerical values based on letter positions in the alphabet, with special handling for the letter 'z'.

## Features

- Convert text strings into numerical values
- Special handling for 'z' character
- Request history tracking
- MySQL database integration
- REST API endpoints
- Logging support

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd last-project
```

2. Create a `.env` file with the following variables:
```
DATABASE_URL=mysql+aiomysql://user:password@db/dbname
MYSQL_DATABASE=dbname
MYSQL_USER=user
MYSQL_PASSWORD=password
MYSQL_ROOT_PASSWORD=rootpassword
```

3. Start the application using Docker Compose:
```bash
docker-compose up -d
```

The API will be available at `http://localhost:8090`

## API Endpoints

### GET /convert
Convert text using query parameter:
```
GET /convert?text=abcee
```

### POST /convert
Convert text using JSON body:
```
POST /convert
Content-Type: application/json

{
    "text": "abcee"
}
```

### GET /history
Retrieve conversion history:
```
GET /history
```

## Example Conversions

- `abcee` → `[2, 10]`
  - a(1) takes b=2
  - c(3) takes ee=5+5=10
- `aza` → `[27]`
  - a(1) takes z+a=27
- `bcd` → `[3]`
  - b(2) takes cd=3+4=7

## Development

To run the application locally without Docker:

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Set up your MySQL database and update the DATABASE_URL

3. Run the application:
```bash
python main.py
```

## Logging

Logs are stored in `application.log` with:
- 7-day rotation
- 14-day retention
- INFO level logging