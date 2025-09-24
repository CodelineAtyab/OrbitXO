# Use Python base image
FROM python:3.10-slim

# Set work directory inside container
WORKDIR /app

# Install Flask
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py .

# Expose port 5000
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
