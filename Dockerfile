# Base Image
FROM python:3.11-slim

# working directory
WORKDIR /app

# copy needed files
COPY app /app/app
COPY ML /app/ML
COPY templates /app/templates
COPY requirements.txt /app

# install dependency
RUN pip install --no-cache-dir -r requirements.txt

# expose port
EXPOSE 5000

# start app
CMD ["python3", "app/app.py"]
