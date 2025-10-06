# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY version.txt .
COPY CHANGELOG.md .

# Create folders for SQLite database and logs
RUN mkdir -p /app/data /app/logs

# Declare volumes for persistence
VOLUME /app/data
VOLUME /app/logs

# Expose port
EXPOSE 8080

# Run FastAPI
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
