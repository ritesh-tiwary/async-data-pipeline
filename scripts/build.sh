export DOCKER_BUILDKIT=1
export COMPOSE_BAKE=true

docker-compose --profile app --file docker-compose.yml build --no-cache 
docker-compose --profile app up --detach