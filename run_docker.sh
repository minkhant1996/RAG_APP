#!/bin/bash

# Check if the first argument (command) was provided
if [ -z "$1" ]; then
  echo "Usage: ./docker.sh {up|down|build|restart} {dev}"
  exit 1
fi

# Set default compose file if not provided
compose_file="docker-compose.dev.yml"

# Check if the second argument (environment) was provided
if [ "$2" == "dev" ]; then
  compose_file="docker-compose.dev.yml"
else
  echo "Invalid environment: $2"
  echo "Usage: ./docker.sh {up|down|build} {dev}"
  exit 1
fi

# Run Docker Compose with the specified command and file
case "$1" in
  up)
    docker-compose -f $compose_file up -d
    ;;
  down)
    docker-compose -f $compose_file down
    ;;
  build)
    docker-compose -f $compose_file up --build
    ;;
  restart)
    docker-compose -f $compose_file down
    docker-compose -f $compose_file up -d
    ;;
  *)
    echo "Invalid option: $1"
    echo "Usage: ./docker.sh {up|down|build|restart} {dev}"
    exit 1
    ;;
esac
