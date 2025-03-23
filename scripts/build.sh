export DOCKER_BUILDKIT=1
export COMPOSE_BAKE=true

docker-compose --file docker-compose.yml build --no-cache
docker-compose up --detach