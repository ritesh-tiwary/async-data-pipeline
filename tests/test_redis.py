import redis


# Redis connection details
redis_host = 'localhost'
redis_port = 6379
redis_password = None

try:
    r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    response = r.ping()
    if response:
        print("Connected to Redis!")
    else:
        print("Ping failed.")
except redis.ConnectionError as e:
    print(f"Redis connection error: {e}")
