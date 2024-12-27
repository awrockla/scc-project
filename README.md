# SCC Project

## Project Overview
Run this app using the following command. Ensure that the Python version is compatible within the container or virtual environment:
```bash
python3 app/app.py
```

---

## Docker

Run the Docker container (**sudo** is not needed on macOS):

1. **Build the container:**
   ```bash
   sudo docker buildx build -t sms-spam-detector-webapp .
   ```
   
   **Alternative (recommended!) Build:**
   ```bash
   docker build --pull . -t sms-spam-detector-webapp:latest
   ```

2. **Run the container:**
   ```bash
   sudo docker run -d --name sms-spam-detector-container -p 5005:5000 sms-spam-detector-webapp
   ```

### Check if the Container is Running
```bash
docker ps
```

### Useful Docker Commands
- **Remove old container:**
  ```bash
  sudo docker rm sms-spam-detector-container
  ```
- **Remove old images:**
  ```bash
  sudo docker image prune -f
  ```
- **Build without cache:**
  ```bash
  sudo docker build --no-cache -t sms-spam-detector-webapp .
  ```

---

## Kubernetes

1. **Create Deployment:**
   ```bash
   kubectl apply -f kubernetes/deployment.yaml
   ```
2. **Expose Deployment:**
   ```bash
   kubectl expose deployment sms-spam-detector-webapp --type=LoadBalancer --port=5000
   ```
3. **Create Tunnel:**
   ```bash
   minikube service sms-spam-detector-webapp 
   ```

### Useful Kubernetes Commands
- **Dashboard:** minikube dashboard
- **View Pods/Services/Deployments:** kubectl get deployments/pods/services
- **Read Logs:** kubectl logs "id"
- **Describe:** kubectl describe "type" "id"

---
