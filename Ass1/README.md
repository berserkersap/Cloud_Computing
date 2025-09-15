# Cloud Computing Assignment 1: Autoscaling Analysis (FASTAPI)
---

This project uses the FastAPI framework to fulfill the assignment requirements, including specific output formats and a string reversal task.

Application Overview
Server: A Python FastAPI application with one endpoint: /reverse (for string reversal).

Client: An asynchronous Python script that takes the user's roll number and test parameters to generate the four required output files in the specified format.

---
# Local Docker Swarm & Kubernetes

The below contains Step-by-step instructions to build, deploy, test and collect outputs for the assignment **locally** using **Docker Swarm** and **Kubernetes (Minikube / Docker Desktop)**.

---

## Repository layout (important files)

* `fastapi_server.py` or `main.py` — FastAPI server (one of these should contain the `app` object)
* `request_client.py` — Client that runs the 10-string test and high-load RPS tests
* `Dockerfile` — Container image build file
* `kubernetes_deployment.yaml` — Deployment + Service manifest for Kubernetes
* `kubernetes_horizontal_pod_autoscaler.yaml` — HPA manifest (minReplicas: 3, maxReplicas: 10)
* `requirements.txt` — Python packages (fastapi, uvicorn\[standard], aiohttp, requests, ...)

> **Make sure the Python server filename matches the Dockerfile CMD**. If `Dockerfile` references `fastapi_server:app` but your server file is `main.py`, either rename `main.py` → `fastapi_server.py` or edit the Dockerfile `CMD` to use `main:app`.

---

## Prerequisites (local)

* Docker (Desktop on Windows/macOS or Docker Engine on Linux) — make sure Docker daemon is running.
* Python 3.8+ and `pip` on the machine where you run the client.
* `kubectl` installed.
* For Kubernetes local: **Minikube** or Docker Desktop with Kubernetes enabled.

Optional but recommended:

* `make` (for convenience)
* Sufficient ulimit / ephemeral ports for high-RPS tests (when you run 1000+ RPS)

---

# Quick checklist before you begin

1. Ensure Docker daemon is running: `docker info`
2. Install Python deps (client / server):

   ```bash
   pip install -r requirements.txt
   ```
3. Verify the server module name in the Dockerfile (see note above).

---

## A. Docker Swarm (local) — steps and explanation

> Purpose: create a Swarm service with **3 replicas** running your FastAPI server. The Swarm manager exposes the service on port `8000` and load-balances between replicas.

### 1) Build the Docker image

From repository root:

```bash
# build locally (image name used locally)
docker build -t cloud-app-fastapi:latest .
```

**Why**: build an image used by Swarm on the same machine.

### 2) (Optional) Test container locally (single container run)

```bash
# run in detached mode so your terminal is free
docker run -d -p 8000:8000 --name cloud-local -e UVICORN_WORKERS=4 cloud-app-fastapi:latest

# check server health
curl http://localhost:8000/
# Expected: JSON health message
```

**Why**: quick sanity check that container and endpoints work. Stop it if you want to use Swarm on the same port:

```bash
docker stop cloud-local && docker rm cloud-local
```

### 3) Initialize Docker Swarm (one-time)

```bash
docker swarm init
```

**Why**: transforms your Docker engine into a Swarm manager so you can create services with replicas.

### 4) Deploy the Swarm service (3 replicas)

> Use one-line command (works on Linux/macOS and PowerShell). On PowerShell omit `\`.

```bash
docker service create --name cloud-fastapi-service --replicas 3 --publish 8000:8000 cloud-app-fastapi:latest
```

**Why**: `docker service create` launches the requested number of replicas and exposes port 8000 on the host. Swarm automatically load-balances requests between replicas.

### 5) Verify the service

```bash
docker service ls
docker service ps cloud-fastapi-service
docker service inspect --pretty cloud-fastapi-service
```

**Why**: confirm 3 replicas are running and inspect placement.

### 6) Test with client (10 strings and 1000 RPS)

Open a separate terminal (client runs from where you are):

```bash
# 10-string test (detailed file)
python request_client.py <ROLL_NUMBER> http://localhost:8000 dockerswarm 10

# 1000 RPS test (60s, summary output)
python request_client.py <ROLL_NUMBER> http://localhost:8000 dockerswarm 1000
```

**Files produced** (in the directory where you ran client):

* `<ROLL_NUMBER>dockerswarm10.txt` — detailed Original / Reversed entries + average
* `<ROLL_NUMBER>dockerswarm1000.txt` — `average_response_time=...` and count stats

### 7) Cleanup Swarm service when done

```bash
docker service rm cloud-fastapi-service
docker swarm leave --force   # optional if you want to disable Swarm mode
```

---

## B. Kubernetes (local: Minikube or Docker Desktop) — steps and explanation

> Purpose: run the same image in Kubernetes with a **Deployment (replicas:3)** and an **HPA** (min 3, max 10). We'll expose the service and run the client tests against it.

**Note**: If you use Minikube, build the image into minikube's Docker daemon so K8s can pull the local image (or push to a registry). If you use Docker Desktop with Kubernetes, building locally is enough.

### 1) Start Minikube (if using Minikube)

```bash
minikube start --driver=docker
```

**Why**: spins up a local k8s cluster.

### 2) Build image for the cluster

**If using Minikube (recommended)**:

```bash
# option A: build inside minikube's docker daemon (so no push to registry required)
eval $(minikube docker-env)
docker build -t cloud-app-fastapi:latest .
# restore shell (optional): eval $(minikube docker-env -u)
```

**If using Docker Desktop with Kubernetes**:

```bash
# just build locally (k8s uses local image)
docker build -t cloud-app-fastapi:latest .
```

**Why**: Kubernetes needs the image available to its nodes. Using `minikube docker-env` avoids having to push to a remote registry.

### 3) Verify / edit Deployment manifest image

Open `kubernetes_deployment.yaml` and set the image used in the container to `cloud-app-fastapi:latest` if it has a different placeholder.

```yaml
# in kubernetes_deployment.yaml
image: cloud-app-fastapi:latest
```

**Why**: local image tag must match what you built.

### 4) Apply manifests (Deployment + Service + HPA)

```bash
kubectl apply -f kubernetes_deployment.yaml
kubectl apply -f kubernetes_horizontal_pod_autoscaler.yaml
```

Check resources:

```bash
kubectl get pods
kubectl get deployments
kubectl get svc
kubectl get hpa
```

**Why**: create pods and HPA so Kubernetes can scale pods based on CPU.

### 5) Ensure Metrics Server (for HPA)

HPA requires metrics to be available. If you don't have it:

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

Wait a minute and then `kubectl get hpa` should show CPU metrics reading.

### 6) Get a URL to reach the Service

Two approaches:

**A — `minikube` (recommended for local)**

```bash
minikube service hex-encoder-fastapi-service --url
# returns a URL like http://192.168.xx.yy:31337
```

**B — `kubectl port-forward` (works on any k8s)**

```bash
kubectl port-forward svc/hex-encoder-fastapi-service 8000:80
# then use http://localhost:8000 as the server URL in the client
```

**Why**: Your Service type in the YAML maps port 80 → container 8000. `minikube service --url` gives an accessible endpoint. Port-forward creates a local tunnel.

### 7) Run the client (10 & 1000)

**Using the service URL returned above** (example returned URL `http://192.168.49.2:31337`):

```bash
python request_client.py <ROLL_NUMBER> http://<SERVICE_URL> kubernetes 10
python request_client.py <ROLL_NUMBER> http://<SERVICE_URL> kubernetes 1000
```

This will write:

* `<ROLL_NUMBER>kubernetes10.txt`
* `<ROLL_NUMBER>kubernetes1000.txt`

The files are created where you run the client.

### 8) Observe HPA scaling during the 1000 RPS run

In a separate terminal run:

```bash
kubectl get hpa hex-encoder-fastapi-hpa -w
kubectl top pods -n default   # requires metrics-server
```

You should see `REPLICAS` increase as CPU utilization crosses the threshold.

### 9) Cleanup

```bash
kubectl delete -f kubernetes_horizontal_pod_autoscaler.yaml
kubectl delete -f kubernetes_deployment.yaml
# optional: minikube stop && minikube delete
```

---

## Output files — format and where to find them

* `ROLLNUMBERdockerswarm10.txt` / `ROLLNUMBERkubernetes10.txt` — detailed list of the 10 original strings and their reversed results; final line is `average_response_time=x`.

* `ROLLNUMBERdockerswarm1000.txt` / `ROLLNUMBERkubernetes1000.txt` — contains:

  ```
  average_response_time=<seconds>
  requests_sent=<number>
  requests_successful=<number>
  ```

Files are created in the **current working directory** where you executed the `request_client.py` script.

---

## Troubleshooting & common issues

* **Docker commands fail**: ensure Docker Desktop / daemon is running. On Windows enable WSL2 backend in Docker Desktop settings.
* **Port 8000 in use**: stop any local test containers or change `-p` mapping in Docker commands.
* **Kubernetes `kubectl apply` fails with image not found**: you built the image into the wrong Docker daemon. If using Minikube, run `eval $(minikube docker-env)` before `docker build` so the image is available to Minikube.
* **HPA not scaling / metrics not available**: install metrics-server (see step above) and wait a minute for metrics to appear.
* **Client socket errors on high RPS**: the client machine may exhaust ephemeral ports or ulimits. Try from a more powerful machine or run lower RPS per client.

---

## Optional
There is a Makefile for building the image and pushing into the dockerhub repo. However, the username needs to be replaced with destination dockerhub account.
You can use it as 
* Build Image - ```make build```
* Push to DockerHub - ```make push```
* Run Container - ```make run```
* Stop Container - ```make stop```
* Rebuild and Run Fresh - ```make rebuild```
---

## Notes & best practices

* Doing in this way, the server runs in docker/kubernetes and the client requests are sent from your local environment and not from the image.
* For reproducible tests, run the client from a machine in the *same network* as your server (local or same LAN) to avoid external network variability.
* Start with `10` and `1000` tests first. For larger RPS, increase gradually and monitor `kubectl top pods`.
* If you need to change how many uvicorn workers each pod runs, set env `UVICORN_WORKERS` in your Deployment or Docker run command (example: `-e UVICORN_WORKERS=4`).
