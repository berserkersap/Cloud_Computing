Cloud Computing Assignment 1: Autoscaling Analysis (FastAPI Edition)
This project uses the FastAPI framework to demonstrate and evaluate the performance of a containerized application under different loads using Docker Swarm and Kubernetes with autoscaling.

Application Overview
Server: A Python FastAPI application that provides an API endpoint (/encode) to convert a string into its hexadecimal representation. It uses Uvicorn as the ASGI server.

Client: An asynchronous Python script using aiohttp to send requests to the server at a high rate and log the response times.

How to Run
Prerequisites
Docker installed

Kubernetes cluster (e.g., Minikube, GKE, EKS)

kubectl configured

A Docker Hub account

Python 3.x and pip installed

1. Install Client Dependencies
The new client uses aiohttp. Install it first:

pip install aiohttp

2. Build and Push the Docker Image
Navigate to the project's root directory.

Build the image using the FastAPI Dockerfile (replace yourusername):

docker build -t yourusername/cloud-app-fastapi:latest -f Dockerfile-fastapi .

Log in to Docker Hub:

docker login

Push the image:

docker push yourusername/cloud-app-fastapi:latest

3. Deploy on Docker Swarm
Initialize Docker Swarm: docker swarm init

Deploy the service (note the port change to 80:8000):

docker service create --name hex-server-fastapi --replicas 3 -p 80:8000 yourusername/cloud-app-fastapi:latest

4. Deploy on Kubernetes
Important: Edit fastapi_deployment.yaml and replace yourusername/cloud-app-fastapi:latest with your actual image name.

Apply the Kubernetes configurations:

kubectl apply -f fastapi_deployment.yaml
kubectl apply -f fastapi_hpa.yaml

Get the external IP of the service:

kubectl get service hex-encoder-fastapi-service

5. Run the Client Tests
Use the fastapi_client.py script.

For Docker Swarm (replace <DOCKER_IP>):

python fastapi_client.py http://<DOCKER_IP>:80 10 Docker_response_10_fastapi.txt
python fastapi_client.py http://<DOCKER_IP>:80 10000 Docker_response_10000_fastapi.txt

For Kubernetes (replace <K8S_EXTERNAL_IP>):

python fastapi_client.py http://<K8S_EXTERNAL_IP>:80 10 kubernetes_response_10_fastapi.txt
python fastapi_client.py http://<K8S_EXTERNAL_IP>:80 10000 kubernetes_response_10000_fastapi.txt
