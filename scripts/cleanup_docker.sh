#!/bin/bash

echo "Stopping all running containers..."
docker stop $(docker ps -aq)

echo "Removing all containers..."
docker rm $(docker ps -aq)

echo "Removing all images..."
docker rmi $(docker images -q) -f

echo "Removing dangling images..."
docker image prune -a -f

echo "Removing all volumes..."
docker volume rm $(docker volume ls -q)

# echo "Removing all networks..."
# docker network rm $(docker network ls -q)

echo "Cleanup complete!"

echo "Verify Cleanup!"

docker ps

docker images