from pymongo import MongoClient

# MongoDB connection details
MONGO_USER = "admin"
MONGO_PASSWORD = "secret"
MONGO_HOST = "localhost"
MONGO_PORT = "27017"

# Connection URI
mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"

try:
    # Connect to MongoDB
    client = MongoClient(mongo_uri)

    print("All databases:")
    for db_name in client.list_database_names():
        print(f"- {db_name}")

        # List collections for each database
        db = client[db_name]
        collections = db.list_collection_names()
        print(f"  Collections: {', '.join(collections)}")

    print('\nGet celery_taskmeta from a celery_results collection\n')
    db = client['celery_results']
    collection = db['celery_taskmeta']

    # Find document by ID
    document_id = '9b9a062b-1c29-49e0-b9f0-31faf4140126'
    document = collection.find_one({"_id": document_id})
    print(document)

    # Get all documents
    all_docs = collection.find()
    print("\nAll documents:", len(list(all_docs)))

    # Close the connection
    client.close()
except Exception as e:
    print("MongoDB connection error:", e)
