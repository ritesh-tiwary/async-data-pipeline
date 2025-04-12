export DOCKER_BUILDKIT=1
export COMPOSE_BAKE=true

docker-compose build  --no-cache --profile ignore-me backend down --file docker-compose.yml
docker-compose up --detach