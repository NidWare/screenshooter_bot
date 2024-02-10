#!/bin/bash

# Define your container name
CONTAINER_NAME="my-python-app-container"

# Stop the running container
docker stop $CONTAINER_NAME

# Remove the container
docker rm $CONTAINER_NAME

# Uncomment the following line if you also want to remove the Docker image
# docker rmi my-python-app
