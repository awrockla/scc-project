# Base Image: use slim image
FROM python:3.11-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "app/app.py"]

