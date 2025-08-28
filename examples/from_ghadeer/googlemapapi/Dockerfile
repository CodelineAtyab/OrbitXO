# Minimal Dockerfile for your FastAPI app
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy project files
COPY . /app

# Upgrade pip and install requirements (fallback installs common deps if requirements.txt missing)
RUN pip install --upgrade pip \
 && (pip install --no-cache-dir -r requirements.txt || pip install --no-cache-dir fastapi "uvicorn[standard]" python-dotenv requests)

EXPOSE 8000

# Run uvicorn on container start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]