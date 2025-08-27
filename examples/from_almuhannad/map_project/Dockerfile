FROM python:3.11-slim AS builder

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create a clean runtime image
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application files
COPY --from=builder /app /app

# Create a non-root user to run the application
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates \
       curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m appuser \
    && mkdir -p /logs \
    && chown -R appuser:appuser /app /logs \
    && chmod 755 /logs
USER appuser

# Expose the port that the application will run on
EXPOSE 8000

# Command to run the application
CMD ["sh", "-c", "python init_mysql_db.py && uvicorn main:app --host 0.0.0.0 --port 8000"]