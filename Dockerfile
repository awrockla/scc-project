# Base Image: Verwende ein Python-Image basierend auf Alpine
FROM python:3.10-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "app/app.py"]

