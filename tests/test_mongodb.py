from pymongo import MongoClient

# MongoDB connection details
MONGO_USER = "admin"
MONGO_PASSWORD = "secret"
MONGO_HOST = "localhost"
MONGO_PORT = "27017"
MONGO_DB = "admin"

# Connection URI
mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"

try:
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client[MONGO_DB]

    # Test query
    result = db.command("ping")
    print("MongoDB Connected Successfully:", result)

    # Close the connection
    client.close()
except Exception as e:
    print("MongoDB connection error:", e)
