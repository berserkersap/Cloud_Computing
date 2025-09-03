Cloud Computing Assignment 1: Autoscaling Analysis (FASTAPI)
This project uses the FastAPI framework to fulfill the updated assignment requirements, including specific output formats and a string reversal task.

Application Overview
Server: A Python FastAPI application with two endpoints: /encode (for hex encoding) and /reverse (for string reversal).

Client: An asynchronous Python script that takes the user's roll number and test parameters to generate the four required output files in the specified format.

How to Run
Prerequisites
Docker, Kubernetes (kubectl), a Docker Hub account, and Python 3.x installed.

Install client dependency: pip install aiohttp

1. Build and Push the Docker Image
Build the image using the Dockerfile-fastapi file (replace yourusername and choose a new tag like v2).

docker build -t yourusername/cloud-app-fastapi:v2 -f Dockerfile-fastapi .

Log in and push the image:

docker login
docker push yourusername/cloud-app-fastapi:v2

2. Deploy the Service
For Docker Swarm:

docker service create --name hex-server-fastapi --replicas 3 -p 80:8000 yourusername/cloud-app-fastapi:v2

For Kubernetes:

IMPORTANT: Update fastapi_deployment.yaml to use your new image tag (e.g., yourusername/cloud-app-fastapi:v2).

Apply the configs:

kubectl apply -f fastapi_deployment.yaml
kubectl apply -f fastapi_hpa.yaml

3. Run the Updated Client Tests
Use the updated_fastapi_client.py script. It now requires 4 arguments.

Command Format:

python updated_fastapi_client.py <YOUR_ROLL_NUMBER> <SERVER_URL> <platform> <10|10000>

Example Commands (replace with your details):

Docker Swarm - 10 Strings Test:

python updated_fastapi_client.py CB.EN.U4CSE19000 http://<DOCKER_IP> dockerswarm 10

This will create the file CB.EN.U4CSE19000dockerswarm10.txt

Docker Swarm - 10000 RPS Test:

python updated_fastapi_client.py CB.EN.U4CSE19000 http://<DOCKER_IP> dockerswarm 10000

This will create the file CB.EN.U4CSE19000dockerswarm10000.txt

Kubernetes - 10 Strings Test:

python updated_fastapi_client.py CB.EN.U4CSE19000 http://<K8S_EXTERNAL_IP> kubernetes 10

This will create the file CB.EN.U4CSE19000kubernetes10.txt

Kubernetes - 10000 RPS Test:

python updated_fastapi_client.py CB.EN.U4CSE19000 http://<K8S_EXTERNAL_IP> kubernetes 10000

This will create the file CB.EN.U4CSE19000kubernetes10000.txt****
