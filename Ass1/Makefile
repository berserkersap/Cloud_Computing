# Makefile for FastAPI Reverse String App

# Variables
IMAGE_NAME = cloud-app-fastapi
TAG = latest
CONTAINER_NAME = fastapi-server
PORT = 8000

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME):$(TAG) .

# Run locally (detached mode)
run:
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):8000 $(IMAGE_NAME):$(TAG)

# Stop container
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Rebuild (stop + build + run)
rebuild: stop build run

# Push to Docker Hub (update with your username)
push:
	docker tag $(IMAGE_NAME):$(TAG) <your-dockerhub-username>/$(IMAGE_NAME):$(TAG)
	docker push <your-dockerhub-username>/$(IMAGE_NAME):$(TAG)

# Clean local images
clean:
	docker rmi $(IMAGE_NAME):$(TAG) || true
