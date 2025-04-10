# Use official Redis as base
FROM redis:7-alpine

# Expose the default Redis port
EXPOSE 6379

# Optional: copy a custom Redis config
COPY redis.conf /usr/local/etc/redis/redis.conf

# Start Redis with the custom config (if present)
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
