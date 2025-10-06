FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev gcc dos2unix && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN find . -name "*.py" -exec dos2unix {} +
RUN chmod +x wait-for-db.py

EXPOSE 8000

CMD ["python3", "wait-for-db.py"]
