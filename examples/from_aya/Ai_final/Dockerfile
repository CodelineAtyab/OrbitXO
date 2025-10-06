FROM python:3.11-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

ENV PYTHONUNBUFFERED=1
EXPOSE 8080

# Start the app
CMD ["uvicorn", "app_service:app", "--host", "0.0.0.0", "--port", "8080"]
