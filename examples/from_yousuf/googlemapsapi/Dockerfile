FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app/googlemapsapi

# Install any OS-level deps if needed (keep minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

EXPOSE 8000

# Run the FastAPI app; keep reload off in container (use compose volume for dev)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
