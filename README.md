# scc-project
Project:

run this app with command:
- python3 app/app.py

run docker-container:
1. build the container: sudo docker build -t sms-spam-detector-webapp .
2. run the container: sudo docker run -d --name sms-spam-detector-container -p 5000:5000 sms-spam-detector-webapp

Check if Container is running with: docker ps

More usefull commands:
- sudo docker rm sms-spam-detector-container (remove old container)
- sudo docker image prune -f (remove old images)
- sudo docker build --no-cache -t sms-spam-detector-webapp . (build without cache)