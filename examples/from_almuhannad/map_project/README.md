# Map Project

A containerized FastAPI application for tracking and analyzing travel times between locations using Google Maps API.

## Features

- Track travel times between specified locations
- Record historical travel time data
- Identify and notify about minimum travel times
- Web UI for viewing travel time data
- API endpoints for integration

## Prerequisites

- Docker and Docker Compose installed on your system
- Google Maps API key (for production use)

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/map-project.git
cd map-project
```

### 2. Configure Environment Variables

Copy the example .env file and modify it with your settings:

```bash
cp .env.example .env
```

Edit the .env file and set your Google Maps API key and other configuration:

```
SOURCE=Muscat, Codeline
DESTINATION=Salalah, Oman
API_KEY=your_google_maps_api_key
SLACK_WEBHOOK_URL=your_slack_webhook_url
```

### 3. Build and Run with Docker Compose

```bash
docker-compose up -d
```

This will:
- Build the Docker image
- Initialize the SQLite database
- Start the application on port 8000

### 4. Access the Application

- Web UI: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## API Endpoints

- `/` - Web UI for viewing travel time data
- `/health` - Health check endpoint
- `/api-info` - Basic API information
- `/travel-time` - Get travel time between locations
- `/historical-data` - Get historical travel time data
- `/config` - Get current configuration

## Development

### Building the Docker Image Manually

```bash
docker build -t map-project:latest .
```

### Running the Container Manually

```bash
docker run -p 8000:8000 --env-file .env map-project:latest
```

## License

[Add your license information here]

## Acknowledgements

- FastAPI
- Google Maps API
- [Any other acknowledgements]
