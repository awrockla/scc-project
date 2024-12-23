# scc-project
Project:

run this app with command (careful! the python version should be given within the container or the virtual environment):
- python3 app/app.py

run docker-container (**sudo** is not needed - at least not on mac):
1. build the container: sudo docker buildx build -t sms-spam-detector-webapp .
<b>
1.1: alternativ (empfohlen!) Build: docker build --pull . -t sms-spam-detector-webapp:latest
</b>
2. run the container: sudo docker run -d --name sms-spam-detector-container -p 5005:5000 sms-spam-detector-webapp

Check if Container is running with: docker ps

More usefull commands:
- sudo docker rm sms-spam-detector-container (remove old container)
- sudo docker image prune -f (remove old images)
- sudo docker build --no-cache -t sms-spam-detector-webapp . (build without cache)
