# from pymongo import MongoClient


# # MongoDB connection details
# MONGO_HOST = "mongodb_broker"
# MONGO_PORT = "27017"
# MONGO_USER = "admin"
# MONGO_PASSWORD = "secret"
# MONGO_DB = "testdb"

# # Connection URI with authentication
# mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"
# # mongodb://<credentials>@127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.4.2
# print(mongo_uri)

# try:
#     # Connect to MongoDB
#     client = MongoClient(mongo_uri)
#     db = client[MONGO_DB]

#     # Insert a test document
#     db.test_collection.insert_one({"message": "MongoDB Connection Successful!"})

#     # Retrieve the inserted document
#     result = db.test_collection.find_one()
#     print("Test Document:", result)

#     # Close the connection
#     client.close()

# except Exception as e:
#     print("MongoDB connection error:", e)

from pymongo import MongoClient

# MongoDB connection details
MONGO_USER = "admin"
MONGO_PASSWORD = "secret"
MONGO_HOST = "mongodb_broker"  # Use the exact container name
MONGO_PORT = "27017"  # Default MongoDB port
MONGO_DB = "admin"  # Use the correct database (likely "admin")

# Connection URI
mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin"

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
