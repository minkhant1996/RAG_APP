#!/bin/bash

# Define the Docker container and image
CONTAINER_NAME="redis"
IMAGE_NAME="redis:latest"  # Replace with your Redis image version if needed

# Function to run the container
run_container() {
    echo "Starting the Redis Docker container..."
    docker run -d --name $CONTAINER_NAME -p 6379:6379 $IMAGE_NAME
    echo "Redis Docker container started with name: $CONTAINER_NAME"
}

# Function to restart the container
restart_container() {
    echo "Restarting the Redis Docker container..."
    docker restart $CONTAINER_NAME
    echo "Redis Docker container restarted."
}

# Check for argument
if [ $# -eq 0 ]; then
    echo "No arguments provided. Please specify 'run' or 'restart'."
    exit 1
fi

# Argument processing
case $1 in
    run)
        # Check if the container already exists
        if docker ps -a --format '{{.Names}}' | grep -Eq "^${CONTAINER_NAME}$"; then
            echo "Container already exists. Please use 'restart' to restart it."
        else
            run_container
        fi
        ;;
    restart)
        # Check if the container is running
        if docker ps --format '{{.Names}}' | grep -Eq "^${CONTAINER_NAME}$"; then
            restart_container
        else
            echo "Container is not running. Use 'run' to start it."
        fi
        ;;
    *)
        echo "Invalid argument. Use 'run' or 'restart'."
        exit 1
        ;;
esac
