FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main_app.py .
COPY measurement_converter.py .
COPY database_manager.py .
COPY version.txt .
COPY CHANGELOG.md .

# Create logs directory
RUN mkdir -p /app/logs

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "main_app.py", "8000"]