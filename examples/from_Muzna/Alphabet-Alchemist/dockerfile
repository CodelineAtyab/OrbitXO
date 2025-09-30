# Use a lightweight Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy requirements first for efficient caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Create logs directory inside container
RUN mkdir -p logs

# Expose application port
EXPOSE 8888

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main_app:app", "--host", "0.0.0.0", "--port", "8888"]
