RUN echo "Building the Docker image for SMS Spam Detector..."

# Base Image
FROM python:3.10.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "app/app.py"]
