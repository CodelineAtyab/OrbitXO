FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create log folder
RUN mkdir -p logs && touch logs/app.log

# Expose port
EXPOSE 8080

# Run Flask app
CMD ["python", "main_app.py"]
