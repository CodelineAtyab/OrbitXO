FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main_app.py .
COPY parser.py .
COPY log_config.py .

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["python", "main_app.py"]