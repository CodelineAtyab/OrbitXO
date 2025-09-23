# Monitoring FastAPI with Prometheus and Grafana

I'll help you set up a complete monitoring solution for your FastAPI application and Ubuntu system metrics using Prometheus and Grafana with Docker. This solution will allow you to monitor:

- FastAPI application metrics (request counts, latency, errors)
- Ubuntu system metrics (CPU, RAM, disk usage)

## Overview of the Solution

1. **FastAPI Application**: Instrument your FastAPI app to expose Prometheus metrics
2. **Node Exporter**: Collect system metrics from Ubuntu
3. **Prometheus**: Scrape and store metrics from both sources
4. **Grafana**: Visualize the metrics with dashboards

## Step-by-Step Implementation

### 1. Instrument Your FastAPI Application

First, add Prometheus metrics to your FastAPI application:

```bash
pip install prometheus-fastapi-instrumentator
```

Update your FastAPI application:

```python name=main.py
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Initialize instrumentator
Instrumentator().instrument(app).expose(app)

# Your existing endpoints
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Add more endpoints as needed
```

### 2. Create Docker Compose Configuration

Create a `docker-compose.yml` file in your project root:

```yaml name=docker-compose.yml
version: '3'

services:
  fastapi:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    networks:
      - monitoring

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
    networks:
      - monitoring

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    restart: unless-stopped
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.rootfs=/rootfs'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    ports:
      - "9100:9100"
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    networks:
      - monitoring

networks:
  monitoring:
    driver: bridge

volumes:
  prometheus_data:
  grafana_data:
```

### 3. Create a Dockerfile for Your FastAPI App

```dockerfile name=Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4. Create requirements.txt

```text name=requirements.txt
fastapi
uvicorn
prometheus-fastapi-instrumentator
```

### 5. Configure Prometheus

Create a directory for Prometheus configuration:

```bash
mkdir -p prometheus
```

Create the Prometheus configuration file:

```yaml name=prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'fastapi'
    static_configs:
      - targets: ['fastapi:8000']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
```

### 6. Configure Grafana Dashboards

Create the Grafana provisioning directories:

```bash
mkdir -p grafana/provisioning/datasources
mkdir -p grafana/provisioning/dashboards
```

Create a Prometheus datasource for Grafana:

```yaml name=grafana/provisioning/datasources/datasource.yml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
    access: proxy
    isDefault: true
```

### 7. Start the Monitoring Stack

```bash
docker-compose up -d
```

## Accessing Your Monitoring Tools

- **FastAPI**: http://localhost:8000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (login with admin/admin)

## Setting Up Grafana Dashboards

After logging into Grafana:

1. Go to Dashboards > Import
2. Import these dashboard IDs:
   - **1860**: Node Exporter Full (for Ubuntu system metrics)
   - **14282**: FastAPI Metrics Dashboard

Alternatively, you can create custom dashboards with panels for:

- System CPU Usage
- System Memory Usage
- Disk Usage
- FastAPI Request Count
- FastAPI Response Time
- HTTP Error Rate

## Best Practices

1. **Security**: Change default Grafana credentials in production
2. **Persistence**: The setup includes volumes for Prometheus and Grafana data
3. **Alerting**: Configure Grafana alerts for critical metrics
4. **Custom Metrics**: Add application-specific metrics using the Prometheus client library

Would you like me to explain any specific part in more detail or help with customizing any particular aspect of this monitoring setup?