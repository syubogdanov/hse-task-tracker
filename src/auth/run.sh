docker compose down || true

docker compose up \
    --build \
    --force-recreate \
    --remove-orphans
