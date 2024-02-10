#!/bin/bash

# Define your image and container names
IMAGE_NAME="my-python-app"
CONTAINER_NAME="my-python-app-container"

# Pull the latest changes from Git
git pull origin main

# Build the new Docker image
docker build -t $IMAGE_NAME .

# Stop and remove any existing container
docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME

# Run the container from the new image
docker run -d --name $CONTAINER_NAME -p 4000:80 --restart unless-stopped $IMAGE_NAME
