FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create logs directory
RUN mkdir -p /app/logs

COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8010

# Command to run the API
CMD ["uvicorn", "alphabet_encoder:app", "--host", "0.0.0.0", "--port", "8010"]