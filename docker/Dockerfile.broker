# Use official Redis as base
FROM redis:7-alpine

# Optional: copy a custom Redis config
COPY redis.conf /usr/local/etc/redis/redis.conf

# Start Redis with the custom config (if present)
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
